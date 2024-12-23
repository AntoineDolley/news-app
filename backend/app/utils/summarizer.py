from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from ..config import settings
import os
import asyncio
import time

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
    start_time = time.time()
    summary = llm.invoke(summary_prompt)
    end_time = time.time()  # Fin du timer
    elapsed_time = end_time - start_time
    print(f"Résumé généré en {elapsed_time:.2f} secondes")

    return summary.strip()

async def generate_summary_async(text: str) -> str:
    """
    Génère un résumé d'une phrase pour un texte donné en utilisant OpenAI (asynchrone).

    Parameters:
        text (str): Le texte à résumer.

    Returns:
        str: Le résumé généré.
    """
    return await asyncio.to_thread(generate_summary, text)