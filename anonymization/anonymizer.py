from mistralai import Mistral
import os
import json

class Anonymizer:
    def __init__(self):
        FORMAT ="""
        {
            "texte": "texte d'origine",
            "anonymisation": "texte anonymisé",
            "justification": "justification de l'anonymisation"
        }
        """

        self.AIPrompt = f"""
            Vous êtes un modèle de langage spécialisé dans la détection et l'anonymisation des informations personnelles (PII) dans les textes.
            Votre tâche consiste à identifier les PII telles que les noms, adresses, numéros de téléphone, adresses e-mail, numéros de sécurité sociale, 
            et autres informations sensibles, puis à les remplacer par des déterminants et pronoms impersonnels appropriés.
            Vous ne devez pas corriger les fautes d'orthographes, de grammaires ou de syntaxes.
            Si le texte ne contient aucune informations personnelles, renvoyer le texte d'origine.


            Instructions :
            1. Détection des PII : Identifiez toutes les informations personnelles dans le texte fourni.
            2. Remplacement : Remplacez chaque PII détectée par un déterminant ou pronom impersonnel approprié. 
            Par exemple, remplacez les noms par "quelqu'un", les adresses par "un endroit", les numéros de téléphone par "un numéro", etc.
            3. Conservation du sens : Assurez-vous que le texte modifié conserve le sens original autant que possible.

            Format de réponse:
            Répondre uniquement selon le format JSON :
            {FORMAT}

            Votre réponse en objet JSON:
        """
        self.client = Mistral(api_key=os.environ['SIRIUS_MISTRAL_API_KEY'])

    def anonymize(self, text):
        UserPrompt = f"""
            Voici un témoignage à corriger:
            ```
            {text}
            ```
        """

        messages = [
            {
                "role": "system",
                "content": self.AIPrompt},
            {
                "role": "user",
                "content": UserPrompt,
            }
        ]

        response = self.client.chat.complete(
            model = "mistral-small-latest",
            messages = messages,
            response_format = {
                "type": "json_object",
            }
        )
        res = json.loads(response.choices[0].message.content)
        return res