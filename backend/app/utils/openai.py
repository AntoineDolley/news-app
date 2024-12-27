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
    Generates a concise and informative summary for the given text using OpenAI.

    Parameters:
        text (str): The text to summarize.

    Returns:
        str: The generated summary.
    """
    # Enhanced prompt template for better summaries
    template = """
    You are an expert summarizer. Your task is to create a clear and concise summary of the following text.
    
    Guidelines:
    - The summary should not exceed 3 sentences.
    - Focus on the main ideas and omit unnecessary details.
    - Avoid repetition and redundancy.
    - Make sure the summary is in fluent and grammatically correct English.

    Text:
    {text}

    Summary:
    """

    # Create the prompt
    prompt = PromptTemplate(input_variables=["text"], template=template)
    summary_prompt = prompt.format(text=text)

    # Generate the summary
    start_time = time.time()
    summary = llm.invoke(summary_prompt)
    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time
    print(f"Summary generated in {elapsed_time:.2f} seconds")

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

async def generate_summary_and_title_async(text: str, cluster_id: int) -> tuple:
    """
    Génère un résumé et un titre pour un texte donné en utilisant OpenAI (asynchrone).

    Parameters:
        text (str): Le texte à résumer.
        cluster_id (int): L'identifiant du cluster.

    Returns:
        tuple: (cluster_id, dict) où dict contient le résumé et le titre.
    """
    summary_and_title = await asyncio.to_thread(generate_summary_and_title, text)
    return cluster_id, summary_and_title


async def generate_summaries_for_clusters(cluster_texts):
    tasks = [generate_summary_and_title_async(text) for text in cluster_texts]
    return await asyncio.gather(*tasks)
