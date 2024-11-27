from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from ..config import settings
import os

# Initialiser le modèle OpenAI
openai_api_key = settings.OPENAI_API_KEY 
llm = OpenAI(temperature=0.9, openai_api_key=openai_api_key)

def generate_summary(text: str) -> str:
    """
    Génère un résumé d'une phrase pour un texte donné en utilisant OpenAI.

    Parameters:
        text (str): Le texte à résumer.

    Returns:
        str: Le résumé généré.
    """
    # Modèle de prompt pour le résumé
    template = """
    Summarize the following text:
    
    {text}
    """

    # Créer le prompt
    prompt = PromptTemplate(input_variables=["text"], template=template)
    summary_prompt = prompt.format(text=text)

    # Générer le résumé
    summary = llm(summary_prompt)

    return summary.strip()
