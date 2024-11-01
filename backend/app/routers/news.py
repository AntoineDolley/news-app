from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db
from ..utils.fetch_news import fetch_news

router = APIRouter()

@router.get("/news", response_model=List[schemas.Article])
def read_news(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles

@router.get("/news/search", response_model=List[schemas.Article])
def search_news(q: str, db: Session = Depends(get_db)):
    articles_data = fetch_news(q)
    articles = []
    for article_data in articles_data:
        article_create = schemas.ArticleCreate(**article_data)
        db_article = crud.create_article(db, article_create)
        articles.append(db_article)
    return articles
