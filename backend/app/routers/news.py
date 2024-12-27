from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db
import asyncio
from ..crud import update_article_if_needed
from app.schemas import Article as ArticleSchema
from ..clustering import workflow_query_cluster_and_summarize

router = APIRouter()

@router.get("/", response_model=schemas.NewsResponse)
async def read_news(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> schemas.NewsResponse:
    """
    Retrieve a list of recent news articles and their clusters.
    """
    try:
        articles = crud.get_latest_articles(db, skip=skip, limit=limit)
    except Exception as e:
        print(f"[ERROR] Failed to fetch latest articles: {e}")
        return schemas.NewsResponse(articles=[], clusters=[])
    
    try:
        # Mettre à jour les résumés manquants en parallèle
        updated_articles = await asyncio.gather(
            *(crud.update_article_if_needed(db, article) for article in articles)
        )
    except Exception as e:
        print(f"[ERROR] Failed to update article summaries: {e}")
        updated_articles = articles  # Revenir aux articles non mis à jour

    try:
        # Effectuer le clustering et générer les résumés/titres des clusters en thread séparé
        cluster_summaries = await asyncio.to_thread(workflow_query_cluster_and_summarize, updated_articles)
    except Exception as e:
        print(f"[ERROR] Failed to perform clustering and summarization: {e}")
        cluster_summaries = {}
    
    # Préparer la réponse
    clusters_json = []
    for cluster_id, info in cluster_summaries.items():
        # Convertir les articles du cluster en instances de schéma Pydantic
        cluster_articles = [
            schemas.Article(**article) for article in info.get("articles", [])
        ]
        clusters_json.append(
            schemas.ClusterSummary(
                cluster_id=cluster_id,
                title=info.get("title", f"Cluster {cluster_id}"),
                summary=info.get("summary", "No summary available."),
                articles=cluster_articles
            )
        )
    
    response = schemas.NewsResponse(
        articles=updated_articles,
        clusters=clusters_json
    )
    
    return response