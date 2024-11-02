import requests
from datetime import datetime
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

def get_db() -> Session:
    """
    Generate a database session for dependency injection.

    Yields:
        Session: A SQLAlchemy database session.

    Ensures:
        The session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

engine = create_engine(
    "sqlite:///C:\\Users\\antoine\\Desktop\\news-app\\database\\news.db",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

url = 'https://newsapi.org/v2/top-headlines'

params = {
    'country' : 'us',
    'apiKey': 'c05f140b4860486cba5633ca73c2f014',
}

response = requests.get(url,params=params)
data = response.json()
articles_data = []
for item in data.get('articles', []):
    article = {
        'title': item.get('title'),
        'summary': item.get('description'),
        'published_at': datetime.strptime(item.get('publishedAt'), '%Y-%m-%dT%H:%M:%SZ'),
        'url': item.get('url'),
        'subjects': []  # Pas de sujets spécifiques
    }
    articles_data.append(article)

print(articles_data)

db = get_db()

articles = []
for article_data in articles_data:
    # Create an ArticleCreate object and store it in the database if it doesn't already exist
    article_create = schemas.ArticleCreate(**article_data)
    db_article = crud.create_article(db, article_create)
    articles.append(db_article)




