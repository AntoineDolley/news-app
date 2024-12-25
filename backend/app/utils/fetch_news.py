import requests
from datetime import datetime
from typing import List, Dict
from ..config import settings
import asyncio
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..utils.openai import generate_embedding
from ..database import SessionLocal
from ..models import Article
from ..crud import add_articles_to_db

def fetch_news_by_date(target_date: datetime.date) -> list:
    """
    Fetch les 100 articles les plus populaires pour une date spécifique.

    Parameters:
        target_date (datetime.date): La date cible pour laquelle récupérer les articles.

    Returns:
        list: Liste des articles formatés pour insertion dans la DB.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        'apiKey': settings.NEWS_API_KEY,
        'from': target_date.isoformat(),
        'to': (target_date + timedelta(days=1)).isoformat(),
        'sortBy': 'popularity',
        'pageSize': 100,
        'language': 'en',
        'q': 'news'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Erreur lors de la récupération des articles: {response.status_code}, {response.text}")

    articles = []
    for item in response.json().get('articles', []):
        articles.append({
            'title': item.get('title'),
            'raw_text': item.get('content') or item.get('description'),
            'summary': None,  # Résumé sera éventuellement ajouté plus tard
            'published_at': datetime.fromisoformat(item['publishedAt'][:-1]),
            'url': item.get('url')
        })
    return articles

def populate_function():
    """
    Fonction pour récupérer et insérer les articles les plus populaires d'une date donnée.
    À chaque appel, elle remonte d'un jour si des articles pour cette date existent déjà.
    """
    db: Session = SessionLocal()
    target_date = datetime.utcnow().date() - timedelta(days=2)

    while True:
        # Vérifier si des articles pour la date cible existent déjà
        articles_for_date = db.query(Article).filter(Article.published_at >= target_date,
                                                     Article.published_at < target_date + timedelta(days=1)).all()

        if articles_for_date:
            print(f"[INFO] Articles déjà présents pour le {target_date}, passage au jour précédent.")
            target_date -= timedelta(days=1)
        else:
            break

    print(f"[INFO] Récupération des articles pour le {target_date}.")
    
    # Fetch des articles pour cette date via l’API
    articles_data = fetch_news_by_date(target_date)
    
    # Utilisation de la fonction `add_articles_to_db`
    add_articles_to_db(db, articles_data)

    db.close()
