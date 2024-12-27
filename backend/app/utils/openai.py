import openai
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from ..config import settings
import os
import asyncio
import time

# Initialiser les embeddings OpenAI
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=settings.OPENAI_API_KEY
)
# Initialiser le modèle OpenAI
openai_api_key = settings.OPENAI_API_KEY 
llm = OpenAI(temperature=0.9, openai_api_key=openai_api_key)

def generate_embedding(text: str) -> list:
    """
    Génère un embedding pour un texte donné en utilisant OpenAI via LangChain.

    Parameters:
        text (str): Le texte à encoder.

    Returns:
        list: L'embedding généré.
    """

    embedding = embeddings.embed_query(text)
    return embedding

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

def generate_summary_and_title(cluster_text: str) -> dict:
    """
    Génère un résumé et un titre pour un texte donné en utilisant OpenAI.

    Parameters:
        cluster_text (str): Le texte regroupé des articles d'un cluster.

    Returns:
        dict: Un dictionnaire contenant le résumé et le titre.
    """
    # Prompt pour résumé et titre
    template = """
    You are a professional summarizer. Analyze the following text and perform the following tasks:
    
    1. Generate a concise summary of no more than 2-3 sentences.
    2. Propose a title that represents the topic discussed in the text.
    
    Text:
    {text}
    
    Provide your response in the following format:
    Summary: <summary>
    Title: <title>
    """

    # Créer le prompt
    prompt = PromptTemplate(input_variables=["text"], template=template)
    formatted_prompt = prompt.format(text=cluster_text)

    # Appeler l'API OpenAI
    response = llm.invoke(formatted_prompt)
    
    # Extraire le résumé et le titre
    summary, title = None, None
    if "Summary:" in response and "Title:" in response:
        parts = response.split("Summary:")[1].strip().split("Title:")
        summary = parts[0].strip()
        title = parts[1].strip()

    return {"summary": summary, "title": title}

async def generate_summary_and_title_async(text: str) -> str:
    """
    Génère un résumé d'une phrase pour un texte donné en utilisant OpenAI (asynchrone).

    Parameters:
        text (str): Le texte à résumer.

    Returns:
        str: Le résumé généré.
    """
    return await asyncio.to_thread(generate_summary_and_title, text)
