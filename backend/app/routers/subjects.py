from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app import schemas, crud
from backend.app.dependencies import get_db
from backend.app.utils.fetch_news import fetch_news_by_keyword

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
def search_news(q: str, db: Session = Depends(get_db)) -> List[schemas.Article]:
    """
    Search for news articles by a given keyword.

    Parameters:
        q (str): The search keyword.
        db (Session): The database session dependency.

    Returns:
        List[schemas.Article]: A list of articles matching the search keyword.
    """
    articles_data = fetch_news_by_keyword(q)
    articles = []
    for article_data in articles_data:
        # Create an ArticleCreate object and store it in the database if it doesn't already exist
        article_create = schemas.ArticleCreate(**article_data)
        db_article = crud.create_article(db, article_create)
        articles.append(db_article)
    return articles
