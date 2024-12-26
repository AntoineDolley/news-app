from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db
import asyncio
from ..crud import update_article_if_needed
from app.schemas import Article as ArticleSchema

router = APIRouter()

@router.get("/", response_model=List[schemas.Article])
async def read_news(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[schemas.Article]:
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
        articles = crud.get_latest_articles(db, limit=limit)
    except :
        return []  # Renvoie une liste vide si aucun article n'est trouvé

    updated_articles = await asyncio.gather(
        *(update_article_if_needed(db, article) for article in articles)
    )

    return [ArticleSchema.from_orm(article) for article in updated_articles]
