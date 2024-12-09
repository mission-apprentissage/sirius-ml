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
            Vous êtes un service d'anonymisation automatique qui doit supprimer ou remplacer les noms propres par leur pronom équivalent.

            Instructions:
            - Votre tâche consiste à identifier les noms propres (tel que prénoms et noms de famille) puis à supprimer ou les remplacer par des pronoms appropriés.
            - Vous devez conserver le sens et la forme du texte.
            - Vous ne devez pas corriger les fautes d'orthographes, de grammaires ou de syntaxes.
            - Si le texte ne contient aucun nom propre, renvoyer le texte d'origine.

            Exemples:
            - Jeanne et Paul vont à la montagne -> Ils vont à la montagne
            - Salut Jean, j'espère que tu vas bien ? -> Salut, j'espère que tu vas bien ?
            - Je n'aime pas ce que fait Bob, ce n'est pas très intéressant -> Je n'aime pas ce qu'il fait, ce n'est pas très intéressant

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