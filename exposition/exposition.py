from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage
import os
import json

def expose_function(testimony, categories=''):
    if categories == '':
        categories = {
            'Intégration et ambiance': 'oui|non',
            'Apprentissage du métier': 'oui|non',
            'Horaires': 'oui|non',
            'Rythme entreprise - établissement scolaire': 'oui|non',
            'Avoir moins de vacances': 'oui|non',
            'Journée-type en entreprise' : 'oui|non',
            'Ambiance établissement': 'oui|non',
            'Difficulté des cours': 'oui|non',
            'Enseignement proposé par établissement': 'oui|non',
            'Equipements mis à disposition': 'oui|non',
            'Accessibilité pour les personnes en situation de handicap': 'oui|non',
            'Charge de travail': 'oui|non',
            'Journée-type en établissement' : 'oui|non',
        }

    AIPrompt = f"""
        Indiquer si un témoignage aborde un ou plusieurs sujets en fonction des catégories suivantes:
        ```
        - {'|'.join(list(categories.keys()))}
        ```

        Votre réponse doit obligatoirement être au format JSON suivant:
        {str(categories)}

        Si le témoignage ne fournit pas assez d'informations ou avec un contenu non-significatif,
        renvoyer une réponse négative pour toutes les catégories.

        Votre réponse en JSON sans commentaire ou justification:
    """

    UserPrompt = f"""
        Voici un témoignage à catégoriser:
        ```
        {testimony}
        ```
    """
    chat = ChatMistralAI(mistral_api_key=os.environ['SIRIUS_MISTRAL_API_KEY']).bind(response_format={"type": "json_object"})
    response = chat.invoke(
        [
            AIMessage(content=AIPrompt),
            HumanMessage(content=UserPrompt)
        ])
    try:
        return json.loads(response.content)
    except:
        return {key:"non" for key in categories.keys()}


def correct_function(testimony='', instructions=''):
    FORMAT ="""
    {
        "correction": "texte corrigé",
        "modification": "oui|non si le texte corrigé est différent du texte d'origine"
        "justification": "justification de la correction"
    }
    """

    if instructions == '':
        instructions = """
        - Corrigez uniquement les fautes d'orthographes et de grammaires.
        - Ne pas reformuler le texte.
        - Ne pas remplacer des mots ou groupes de mots par des synonymes.
        - Conserver le même registre de langage.
        - Si le témoignage ne fournit pas assez d'informations ou est incompréhensible, ne rien corriger.
        """

    AIPrompt = f"""
        Vous êtes un correcteur automatique qui doit renvoyer une version corrigée de témoignages écrits.

        Instructions:
        {instructions}

        Réponse attendue:
        Répondre uniquement selon le format suivant:
        {FORMAT}

        Votre réponse en objet JSON:
    """

    UserPrompt = f"""
        Voici un témoignage à corriger:
        ```
        {testimony}
        ```
    """

    chat = ChatMistralAI(
        model="mistral-large-latest",
        mistral_api_key=os.environ['SIRIUS_MISTRAL_API_KEY'],
        temperature=0
        ).bind(response_format={"type": "json_object"})

    response = chat.invoke(
        [
            AIMessage(content=AIPrompt),
            HumanMessage(content=UserPrompt)
        ])

    try:
        return json.loads(response.content)
    except:
        return {'correction': '', 'justification': ''}


def anonymize_function(testimony='', instructions=''):
    FORMAT ="""
    {
        "anonymisation": "texte anonymisé",
        "modification": "oui|non si le texte anonymisé est différent du texte d'origine"
        "justification": "justification de l'anonymisation"
    }
    """

    if instructions == '':
        instructions = """
        - Identifiez les prénoms et noms de famille puis les supprimer ou les remplacer par des pronoms appropriés.
        - Conserver le sens et la forme du texte.
        - Ne pas corriger les fautes d'orthographes, de grammaires ou de syntaxes.
        - Si le texte ne contient aucun nom propre, renvoyer le texte d'origine.

        Exemples:
        - Jeanne et Paul vont à la montagne -> Ils vont à la montagne
        - Salut Jean, j'espère que tu vas bien ? -> Salut, j'espère que tu vas bien ?
        - Je n'aime pas ce que fait Bob, ce n'est pas très intéressant -> Je n'aime pas ce qu'il fait, ce n'est pas très intéressant
        - Bonjour monsieur Dupont !-> Bonjour monsieur !
        """

    AIPrompt = f"""
        Vous êtes un service d'anonymisation automatique qui doit supprimer ou remplacer les prénoms et noms de famille par leur pronom équivalent.

        Instructions:
        {instructions}

        Réponse attendue:
        Répondre uniquement selon le format suivant:
        {FORMAT}

        Votre réponse en objet JSON:
    """

    UserPrompt = f"""
        Voici un témoignage à anonymiser:
        ```
        {testimony}
        ```
    """

    chat = ChatMistralAI(
        mistral_api_key=os.environ['SIRIUS_MISTRAL_API_KEY'],
        temperature=0
        ).bind(response_format={"type": "json_object"})

    response = chat.invoke(
        [
            AIMessage(content=AIPrompt),
            HumanMessage(content=UserPrompt)
        ])

    try:
        return json.loads(response.content)
    except:
        return {'anonymisation': '', 'justification': ''}