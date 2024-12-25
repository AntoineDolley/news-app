from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db
from ..utils.openai import generate_embedding
from ..crud import search_articles_by_similarity, update_article_if_needed
from app.schemas import Article as ArticleSchema
import asyncio


router = APIRouter()

@router.post("/follow", response_model=schemas.User)
def follow_subject(user_name: str, subject_name: str, db: Session = Depends(get_db)) -> schemas.User:
    """
    Follow a subject for a given user.

    Parameters:
        user_name (str): The name of the user who wants to follow a subject.
        subject_name (str): The name of the subject to follow.
        db (Session): The database session dependency.

    Returns:
        schemas.User: The updated user with the followed subject added.

    Raises:
        HTTPException: If the user is not found.
    """
    user = crud.get_user_by_name(db, user_name=user_name)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    subject = crud.get_subject_by_name(db, subject_name=subject_name)
    if not subject:
        subject = crud.create_subject(db, subject_name=subject_name)
    user = crud.add_subject_to_user(db, user, subject)
    return user

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

@router.get("/search", response_model=List[schemas.Article])
async def search_news(q: str, db: Session = Depends(get_db)):
    """
    Recherche des articles similaires basés sur une requête textuelle.
    """
    # Génération de l'embedding pour la requête
    query_embedding = generate_embedding(q)
    
    # Recherche des articles similaires dans la base de données
    similar_articles = search_articles_by_similarity(db, query_embedding)
    
     # Mise à jour des résumés manquants en parallèle
    updated_articles = await asyncio.gather(
        *(update_article_if_needed(db, article) for article in similar_articles)
    )

    # Conversion des articles en dictionnaires compatibles avec le schéma
    return [ArticleSchema.from_orm(article) for article in updated_articles]