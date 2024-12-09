from mistralai import Mistral
import os
import json

class Corrector:
    def __init__(self):
        FORMAT ="""
        {
            "texte": "texte d'origine",
            "correction": "texte corrigé",
            "justification": "justification de la correction"
        }
        """

        self.AIPrompt = f"""
            Vous êtes un correcteur automatique qui doit renvoyer une version corrigée de témoignages écrits.

            Instructions:
            - Vous devez uniquement corriger les fautes d'orthographes et de grammaires.
            - Vous ne devez pas reformuler le texte ou remplacer par des synonymes.
            - Vous devez conserver le même registre de langage.
            - Si le témoignage ne fournit pas assez d'informations ou est incompréhensible, ne rien corriger.

            Réponse attendue:
            Répondre uniquement selon le format suivant:
            {FORMAT}

            Votre réponse en objet JSON:
        """
        self.client = Mistral(api_key=os.environ['SIRIUS_MISTRAL_API_KEY'])

    def correct(self, text):
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
            model = "mistral-large-latest",
            messages = messages,
            response_format = {
                "type": "json_object",
            }
        )
        res = json.loads(response.choices[0].message.content)
        return res



