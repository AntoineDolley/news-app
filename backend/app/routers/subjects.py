from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db
from ..utils.openai import generate_embedding, generate_summary
from ..crud import search_articles_by_similarity, update_article_summary

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
async def search_news(q: str, limit: int = 10, db: Session = Depends(get_db)) -> List[schemas.Article]:
    """
    Recherche des articles en fonction d'une requête textuelle `q`.
    1. Génère un embedding pour `q`.
    2. Recherche les articles les plus proches (via la base vectorielle).
    3. Pour chaque article, génère un résumé s'il n'existe pas.
    4. Retourne la liste des articles.
    """
    # 1. Générer l'embedding
    query_embedding = generate_embedding(q)

    # 2. Rechercher les articles similaires
    articles_dicts = search_articles_by_similarity(db, query_embedding, limit=limit)
    updated_articles = []

    for article_data in articles_dicts:
        if not article_data["summary"]:
            # 3. Générer un résumé et mettre à jour l'article
            new_summary = generate_summary(article_data["raw_text"])
            updated_article = update_article_summary(db, article_data["id"], new_summary)
            updated_articles.append(updated_article)
        else:
            updated_articles.append(article_data)

    # Convertir en liste de schemas.Article
    return [schemas.Article(**a) for a in updated_articles]
