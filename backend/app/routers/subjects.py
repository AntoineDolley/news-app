from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db
from ..utils.openai import generate_embedding
from ..crud import search_articles_by_similarity, update_article_if_needed
from ..clustering import workflow_query_cluster_and_summarize
from app.schemas import Article as ArticleSchema
import asyncio


router = APIRouter()

@router.delete("/follow", response_model=schemas.User)
def unfollow_subject(user_name: str, subject_name: str, db: Session = Depends(get_db)) -> schemas.User:
    """
    Unfollow a subject for a given user.

    Parameters:
        user_name (str): The name of the user who wants to unfollow a subject.
        subject_name (str): The name of the subject to unfollow.
        db (Session): The database session dependency.

    Returns:
        schemas.User: The updated user with the subject removed from followed subjects.

    Raises:
        HTTPException: If the user or subject is not found.
    """
    user = crud.get_user_by_name(db, user_name=user_name)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    subject = crud.get_subject_by_name(db, subject_name=subject_name)
    if not subject:
        raise HTTPException(status_code=404, detail="Sujet non trouvé")
    user = crud.remove_subject_from_user(db, user, subject)
    return user

@router.get("/followed", response_model=List[schemas.Subject])
def get_followed_subjects(user_name: str, db: Session = Depends(get_db)) -> List[schemas.Subject]:
    """
    Retrieve a list of subjects followed by a given user.

    Parameters:
        user_name (str): The name of the user whose followed subjects are being retrieved.
        db (Session): The database session dependency.

    Returns:
        List[schemas.Subject]: A list of subjects followed by the user.

    Raises:
        HTTPException: If the user is not found.
    """
    user = crud.get_user_by_name(db, user_name=user_name)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user.liked_subjects

@router.get("/search", response_model=schemas.NewsResponse)
async def search_news(q: str, db: Session = Depends(get_db)) -> schemas.NewsResponse:
    """
    Recherche des articles similaires basés sur une requête textuelle et retourne les clusters.
    """
    # Génération de l'embedding pour la requête
    query_embedding = generate_embedding(q)
    
    # Recherche des articles similaires dans la base de données
    similar_articles = crud.search_articles_by_similarity(db, query_embedding)
    
    # Mettre à jour les résumés manquants en parallèle
    try:
        updated_articles = await asyncio.gather(
            *(crud.update_article_if_needed(db, article) for article in similar_articles)
        )
    except Exception as e:
        print(f"[ERROR] Failed to update article summaries: {e}")
        updated_articles = similar_articles  # Revenir aux articles non mis à jour
    
    # Effectuer le clustering et générer les résumés/titres des clusters en thread séparé
    try:
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