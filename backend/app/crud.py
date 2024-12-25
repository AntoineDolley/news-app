from sqlalchemy.orm import Session
from typing import List, Optional, Union, Type
from . import models, schemas
from .models import Article
from .utils.auth import get_password_hash, verify_password
from datetime import datetime
import unicodedata
from sqlalchemy.sql import text
from .utils.openai import generate_embedding
from bs4 import BeautifulSoup
from sqlalchemy import desc

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
    return db.query(models.Article).order_by(models.Article.published_at.desc()).offset(skip).limit(limit).all()

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



def search_articles_by_similarity(db: Session, query_embedding: list, limit: int = 10) -> List[Article]:
    """
    Find articles by similarity to a given embedding.

    Parameters:
        db (Session): The database session.
        query_embedding (list): The embedding to compare with.
        limit (int): The maximum number of articles to return.

    Returns:
        List[Article]: A list of similar articles.
    """
    query_embedding_pg = f"[{','.join(map(str, query_embedding))}]"
    return (
        db.query(Article)
        .order_by(Article.embedding.op("<->")(query_embedding_pg))
        .limit(limit)
        .all()
    )

def update_article_summary(db: Session, article_id: int, summary: str) -> Article:
    """
    Update the summary of an article by its ID.

    Parameters:
        db (Session): The database session.
        article_id (int): The ID of the article to update.
        summary (str): The new summary.

    Returns:
        Article: The updated article object.
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if article:
        article.summary = summary
        db.commit()
        db.refresh(article)
    return article

def add_articles_to_db(db: Session, articles_data: list):
    """
    Ajoute une liste d'articles à la base de données après vérification des doublons.

    Parameters:
        db (Session): La session de base de données.
        articles_data (list): La liste des articles à ajouter.
        target_date (str): La date des articles ajoutés (pour le log).

    Returns:
        None
    """

    valid_articles = [
        item for item in articles_data
        if item.get('title') and item['title'] != "[Removed]" and item.get('raw_text')
    ]

    for item in valid_articles:
        item['raw_text'] = BeautifulSoup(item['raw_text'], "html.parser").get_text()[:1000]

    for article in valid_articles:
        # Vérifier si l'article existe déjà via son URL
        existing_article = db.query(Article).filter(Article.url == article['url']).first()
        if existing_article:
            print(f"[INFO] Article déjà existant : {article['title']}")
            continue

        # Générer un embedding pour le contenu brut
        embedding = generate_embedding(article['raw_text'])

        # Créer et insérer l'article
        new_article = Article(
            title=article['title'],
            raw_text=article['raw_text'],
            summary=article.get('summary'),  # Peut être vide si pas fourni
            published_at=article['published_at'],
            url=article['url'],
            embedding=embedding
        )
        db.add(new_article)

    db.commit()

def get_latest_articles(db: Session, limit: int = 10):
    """
    Récupère les articles les plus récents depuis la base de données.

    Parameters:
        db (Session): La session de base de données.
        limit (int): Le nombre maximum d'articles à récupérer.

    Returns:
        List[Article]: Liste des articles les plus récents.
    """
    return db.query(Article).order_by(desc(Article.published_at)).limit(limit).all()