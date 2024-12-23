from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db
from ..utils.fetch_news import fetch_latest_news

router = APIRouter()

@router.get("/", response_model=List[schemas.Article])
def read_news(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[schemas.Article]:
    """
    Retrieve a list of recent news articles.

    Parameters:
        skip (int): The number of articles to skip. Default is 0.
        limit (int): The maximum number of articles to return. Default is 10.
        db (Session): The database session dependency.

    Returns:
        List[schemas.Article]: A list of articles with titles, summaries, publication dates, and URLs.
    """
    try :
        articles = crud.get_articles(db, skip=skip, limit=limit)
    except :
        return []  # Renvoie une liste vide si aucun article n'est trouvé

    return articles



@router.get("/refresh", response_model=List[schemas.Article])
async def latest_news(db: Session = Depends(get_db)):
    """
    Récupère les dernières actualités générales.

    Returns:
        List[schemas.Article]: Liste des articles récents.
    """
    articles_data = await fetch_latest_news()

    articles = []
    for article_data in articles_data:
        # Create an ArticleCreate object and store it in the database if it doesn't already exist
        article_create = schemas.ArticleCreate(**article_data)
        db_article = crud.create_article(db, article_create)
        articles.append(db_article)

    return articles