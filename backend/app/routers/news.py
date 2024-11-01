from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db
from ..utils.fetch_news import fetch_news

router = APIRouter()

@router.get("/news", response_model=List[schemas.Article])
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
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles

@router.get("/news/search", response_model=List[schemas.Article])
def search_news(q: str, db: Session = Depends(get_db)) -> List[schemas.Article]:
    """
    Search for news articles by a given keyword.

    Parameters:
        q (str): The search keyword.
        db (Session): The database session dependency.

    Returns:
        List[schemas.Article]: A list of articles matching the search keyword.
    """
    articles_data = fetch_news(q)
    articles = []
    for article_data in articles_data:
        # Create an ArticleCreate object and store it in the database if it doesn't already exist
        article_create = schemas.ArticleCreate(**article_data)
        db_article = crud.create_article(db, article_create)
        articles.append(db_article)
    return articles
