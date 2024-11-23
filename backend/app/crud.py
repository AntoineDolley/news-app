from sqlalchemy.orm import Session
from typing import List, Optional, Union, Type
from . import models, schemas
from .models import Article
from .utils.auth import get_password_hash, verify_password
from datetime import datetime

def get_user_by_name(db: Session, user_name: str) -> Optional[models.User]:
    """
    Retrieve a user by their username.

    Parameters:
        db (Session): The database session.
        user_name (str): The username of the user.

    Returns:
        Optional[models.User]: The user object if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.username == user_name).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Retrieve a user by their email.

    Parameters:
        db (Session): The database session.
        email (str): The email of the user.

    Returns:
        Optional[models.User]: The user object if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Create a new user with a hashed password.

    Parameters:
        db (Session): The database session.
        user (schemas.UserCreate): The user data for creation.

    Returns:
        models.User: The newly created user object.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        last_connection=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_subject_by_name(db: Session, subject_name: str) -> Optional[models.Subject]:
    """
    Retrieve a subject by its name.

    Parameters:
        db (Session): The database session.
        subject_name (str): The name of the subject.

    Returns:
        Optional[models.Subject]: The subject object if found, otherwise None.
    """
    return db.query(models.Subject).filter(models.Subject.name == subject_name).first()

def create_subject(db: Session, subject_name: str) -> models.Subject:
    """
    Create a new subject with the specified name.

    Parameters:
        db (Session): The database session.
        subject_name (str): The name of the subject to create.

    Returns:
        models.Subject: The newly created subject object.
    """
    db_subject = models.Subject(name=subject_name)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def add_subject_to_user(db: Session, user: models.User, subject: models.Subject) -> models.User:
    """
    Add a subject to the list of subjects followed by the user.

    Parameters:
        db (Session): The database session.
        user (models.User): The user object.
        subject (models.Subject): The subject to add.

    Returns:
        models.User: The updated user object.
    """
    if subject not in user.liked_subjects:
        user.liked_subjects.append(subject)
        db.commit()
        db.refresh(user)
    return user

def remove_subject_from_user(db: Session, user: models.User, subject: models.Subject) -> models.User:
    """
    Remove a subject from the list of subjects followed by the user.

    Parameters:
        db (Session): The database session.
        user (models.User): The user object.
        subject (models.Subject): The subject to remove.

    Returns:
        models.User: The updated user object.
    """
    if subject in user.liked_subjects:
        user.liked_subjects.remove(subject)
        db.commit()
        db.refresh(user)
    return user

def get_articles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Article]:
    """
    Retrieve a list of articles with pagination.

    Parameters:
        db (Session): The database session.
        skip (int): The number of articles to skip.
        limit (int): The maximum number of articles to retrieve.

    Returns:
        List[models.Article]: A list of article objects.
    """
    return db.query(models.Article).offset(skip).limit(limit).all()

def get_article_by_id(db: Session, article_id: int) -> Optional[models.Article]:
    """
    Retrieve an article by its ID.

    Parameters:
        db (Session): The database session.
        article_id (int): The ID of the article.

    Returns:
        Optional[models.Article]: The article object if found, otherwise None.
    """
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def create_article(db: Session, article: schemas.ArticleCreate) -> models.Article:
    """
    Create a new article and associate it with subjects.

    Parameters:
        db (Session): The database session.
        article (schemas.ArticleCreate): The article data for creation.

    Returns:
        models.Article: The newly created article object with associated subjects.
    """
    db_article = models.Article(
        title=article.title,
        summary=article.summary,
        published_at=article.published_at,
        url=article.url
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    # Associate subjects with the article
    for subject_name in article.subjects:
        subject = get_subject_by_name(db, subject_name)
        if not subject:
            subject = create_subject(db, subject_name)
        db_article.subjects.append(subject)
    db.commit()
    db.refresh(db_article)
    return db_article

def authenticate_user(db: Session, username: str, password: str) -> Union[models.User, bool]:
    """
    Authenticate a user by verifying their username and password.

    Parameters:
        db (Session): The database session.
        username (str): The username of the user.
        password (str): The plain text password to verify.

    Returns:
        Union[models.User, bool]: The user object if authentication is successful, False otherwise.
    """
    user = get_user_by_name(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user
