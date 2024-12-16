import pandas as pd
import numpy as np
from datasets import Dataset
import re, os
from transformers import AutoTokenizer, AutoModel
import torch
from tempfile import mkdtemp
from skops import hub_utils
import joblib
from html.parser import HTMLParser
import glob
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage
import json

class Classifier:
    def __init__(self):
        # CamemBERT embeddings model
        camembert_checkpoint = "camembert-base"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(camembert_checkpoint, add_prefix_space=True)
        self.encoder = AutoModel.from_pretrained(camembert_checkpoint, output_hidden_states=True).to(self.device)

        self.models = {}
        for model in ('valid', 'unvalid', 'gem'):
            repo_copy = mkdtemp(prefix="skops")
            repo_id = "apprentissage-sirius/verbatims-"+model
            hub_utils.download(repo_id=repo_id, dst=repo_copy, token=os.environ['SIRIUS_HF_TOKEN'])
            pkl_file = glob.glob(repo_copy + "/*.pkl")[0]
            self.models[model] = joblib.load(pkl_file)

        self.chat = ChatMistralAI(mistral_api_key=os.environ['SIRIUS_MISTRAL_API_KEY']).bind(response_format={"type": "json_object"})
        self.rules = """
            Points positifs :
            1. L'apprentissage permet de se concentrer sur le métier qui correspond à l'apprenti, avec des formations adaptées à ses besoins et sans cours superflus.
            2. Cela permet une entrée progressive dans le monde du travail, en alternant entre le CFA et l'entreprise, ce qui facilite la préparation aux changements.
            3. L'apprenti acquiert une expérience pratique et des compétences dans le métier choisi.
            4. L'apprenti perçoit un salaire, ce qui lui permet de profiter avec ses amis et de gérer son argent.
            5. L'apprentissage offre une plus grande autonomie et maturité.
            6. L'alternance entre l'école et l'entreprise permet de bénéficier d'un accompagnement et d'une expérience professionnelle.
            7. L'apprentissage peut être une alternative intéressante pour ceux qui ont des difficultés avec les études théoriques.
            8. Les apprentis développent une meilleure compréhension de la vie professionnelle et des responsabilités qui y sont liées.
            9. L'apprentissage offre la possibilité de se former à un nouveau métier sans perte financière conséquente.
            10. Les apprentis acquièrent une expérience concrète et assimilent plus rapidement les concepts théoriques en les mettant en pratique.

            Points négatifs :
            1. L'apprentissage implique moins de vacances, généralement seulement 5 semaines par an.
            2. Les apprentis peuvent être stressés par les erreurs commises pendant leur apprentissage.
            3. Certaines entreprises peuvent avoir des attentes irréalistes vis-à-vis des apprentis.
            4. Les apprentis peuvent manquer de connaissances sur les lois et le code du travail, ce qui peut entraîner des problèmes liés aux heures supplémentaires, aux congés et aux horaires de travail.
            5. La recherche d'une entreprise d'accueil peut être difficile et décourageante, surtout pour les femmes dans des métiers traditionnellement masculins.
            6. Les apprentis peuvent souffrir d'un manque de matières générales telles que l'anglais, les mathématiques ou l'histoire-géographie.
            7. Les horaires de travail peuvent être longs et exigeants, avec des journées pouvant durer de 8h à 17h, voire plus, en fonction du métier et de l'entreprise.
            8. Les cours théoriques peuvent être ennuyeux et difficiles à suivre pour certains apprentis, en particulier lorsqu'ils durent plusieurs heures d'affilée.
            9. Les apprentis peuvent se retrouver avec des tâches difficiles dès le début de leur formation, ce qui peut être intimidant.
            10. L'intégration dans une nouvelle équipe peut être difficile, surtout lorsqu'on débute dans le monde professionnel.
        """

        self.format = """
            {
                "avis": "oui|non"
                "score": "score en fonction du nombre de critères d'intérêts évoqués, format float précision 2 chiffres"
                "justification": "justification"
            }
        """

    def __split_text(self, text):
        punctuations = "[.!?;|]+"
        punkts = [0] + [i.end() for i in re.finditer(punctuations, text)] + [len(text)+1]
        indexes = [(punkts[i], punkts[i+1]-1) for i in range(len(punkts)-1) if punkts[i] < punkts[i+1]-1]
        sentences = [text[i[0]:i[1]] for i in indexes]
        return indexes, sentences

    def __clean_text(self, samples):
        text = samples['text']
        text = re.sub("'", " ", text)
        text = re.sub("(\\W)+"," ", text)
        return {'text': text.strip() }

    def __get_hidden_states(self, sent, layers):
        """Push input IDs through model. Stack and sum `layers` (last four by default).
        Select only those subword token outputs that belong to our word of interest
        and average them.
        Args:
            sent (str): Input sentence
            tokenizer : Tokenizer function
            model: bert model
            layers : last 4 model of model
        Returns:
            output: tensor torch
        """
        # encode without adding [CLS] and [SEP] tokens
        encoded = self.tokenizer.encode_plus(sent, return_tensors="pt", add_special_tokens=False)

        with torch.no_grad():
            output = self.encoder(**encoded.to(self.device))

        # Get all hidden states
        states = output.hidden_states
        # Stack and sum all requested layers
        output = torch.stack([states[i] for i in layers]).sum(0).squeeze()
        # Only select the tokens that constitute the requested word
        return output

    def __chunking(self, max_len, sent):
        """because the embedding function is trained on dim 512, so we have to limit the size of the sentences using max_len so the final chunked sentences wont exceed length 512
        Args:
            max_len (int): maximum number of tokens for each chunk
            sent (str): input sentence
        Returns:
            sent_chunk (List(str)): list of chunked sentences
        """
        tokenized_text = sent.lower().split(" ")
        # using list comprehension
        final = [
            tokenized_text[i * max_len : (i + 1) * max_len]
            for i in range((len(tokenized_text) + max_len - 1) // max_len)
        ]

        # join back to sentences for each of the chunks
        sent_chunk = []
        for item in final:
            # make sure the len(items) > 1 or else some of the embeddings will appear as len 1 instead of 768.
            if len(item) > 1:
                sent_chunk.append(" ".join(item))
        return sent_chunk

    # core code for finding agregate word embedding per sentence
    def __aggregate_embeddings(self, sent: str, layers=None, chunk_size=200):
        """Gives the average word embedding per sentence

        Args:
            sent (str): The input sentence

        Returns:
            torch tensor: word embedding per sentence, dim = 768
        """
        # change all standard form numbers to decimal
        np.set_printoptions(formatter={"float_kind": "{:f}".format})

        # Use last four layers by default
        layers = [-4, -3, -2, -1] if layers is None else layers

        # chunking
        chunked_tokens = self.__chunking(chunk_size, sent)  # helper func 3

        # initialise a outside chunk
        word_embedding_avg_collective = []
        word_embedding_sum_collective = []
        word_embedding_max_collective = []

        # for each chunked token, we embed them separately
        for item in chunked_tokens:
            # adding tensors
            word_embedding_torch = self.__get_hidden_states(
                item, layers
            )  # helper fun 2

            # convert torch tensor to numpy array
            word_embedding_np = word_embedding_torch.cpu().detach().numpy()

            word_embedding_avg_chunks = np.mean(word_embedding_np, axis=0)
            word_embedding_avg_collective.append(word_embedding_avg_chunks)

            word_embedding_sum_chunks = np.sum(word_embedding_np, axis=0)
            word_embedding_sum_collective.append(word_embedding_sum_chunks)

            word_embedding_max_chunks = np.amax(word_embedding_np, axis=0)
            word_embedding_max_collective.append(word_embedding_max_chunks)

        word_embedding_avg = np.array([np.float32(0)]*768)
        if len(word_embedding_avg_collective) > 0:
            word_embedding_avg = np.mean(word_embedding_avg_collective, axis=0)

        word_embedding_sum = np.array([np.float32(0)]*768)
        if len(word_embedding_sum_collective) > 0:
            word_embedding_sum = np.sum(word_embedding_sum_collective, axis=0)

        word_embedding_max = np.array([np.float32(0)]*768)
        if len(word_embedding_max_collective) > 0:
            word_embedding_max = np.amax(word_embedding_max_collective, axis=0)

        return {'avg': word_embedding_avg, 'sum': word_embedding_sum, 'max': word_embedding_max}

    # Preprocessing function
    def __embeddings_preprocessing_function(self, examples):
        return self.__aggregate_embeddings(examples['text'], chunk_size=300)

    def __encode(self, text):
        dataset = Dataset.from_dict( {"text": text})
        dataset = dataset.map(self.__clean_text)
        dataset = dataset.map(self.__embeddings_preprocessing_function)
        mean_df = pd.DataFrame(dataset['avg'], columns=['avg_' + str(i+1) for i in range(768)])
        sum_df = pd.DataFrame(dataset['sum'], columns=['sum_' + str(i+1) for i in range(768)])
        max_df = pd.DataFrame(dataset['max'], columns=['max_' + str(i+1) for i in range(768)])
        return pd.concat([mean_df, sum_df, max_df], axis=1)

    # Scores function
    def score(self, text, model):
        emb_text = self.__encode([text])
        scores = self.models[model].predict_proba(emb_text)
        return scores[0]

    # GEM classifier
    def gem_classifier(self, rules, testimony):
        if rules == '':
            rules = self.rules

        AIPrompt = f"""
            Vous êtes un modérateur qui doit publier ou non un témoignage d'expérience positive ou négative en fonction de son intérêt.

            Vos critères d'intérêts sont:
            ```
            {rules}
            ```

            Votre réponse doit obligatoirement être conforme au format JSON suivant:
            {self.format}

            Si le témoignage ne fournit pas assez d'informations ou avec un contenu non-significatif, émettre un avis négatif.

            Votre réponse en JSON:
        """

        UserPrompt = f"""
            Voici un témoignage à modérer:
            ```
            {testimony}
            ```
        """
        response = self.chat.invoke(
            [
                AIMessage(content=AIPrompt),
                HumanMessage(content=UserPrompt)
            ])
        try:
            res = json.loads(response.content)
            res['score'] = float(res['score']) if res['score'] != None else float(0)
            return res

        except:
            return {"avis":"non", "score": 0.0, "justification":"Témoignage non-significatif"}