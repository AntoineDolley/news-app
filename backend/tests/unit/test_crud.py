# tests/unit/test_crud.py

import pytest
from sqlalchemy.orm import Session
from app import crud, models, schemas
from datetime import datetime

def test_create_user(db_session: Session):
    """
    Teste la création d'un nouvel utilisateur.
    """
    user_in = schemas.UserCreate(username="testuser", email="test@example.com", password="testpassword")
    user = crud.create_user(db_session, user=user_in)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password != "testpassword"  # Le mot de passe doit être haché

def test_get_user_by_name(db_session: Session):
    """
    Teste la récupération d'un utilisateur par son nom d'utilisateur.
    """
    # Préparation : création d'un utilisateur
    user_in = schemas.UserCreate(username="testuser", email="test@example.com", password="testpassword")
    crud.create_user(db_session, user=user_in)

    # Test
    user = crud.get_user_by_name(db_session, user_name="testuser")
    assert user is not None
    assert user.username == "testuser"

def test_create_subject(db_session: Session):
    """
    Teste la création d'un nouveau sujet.
    """
    subject_name = "Machine Learning"
    subject = crud.create_subject(db_session, subject_name=subject_name)
    assert subject.name == subject_name

def test_get_subject_by_name(db_session: Session):
    """
    Teste la récupération d'un sujet par son nom.
    """
    # Préparation : création d'un sujet
    subject_name = "Artificial Intelligence"
    crud.create_subject(db_session, subject_name=subject_name)

    # Test
    subject = crud.get_subject_by_name(db_session, subject_name=subject_name)
    assert subject is not None
    assert subject.name == subject_name

def test_add_subject_to_user(db_session: Session):
    """
    Teste l'ajout d'un sujet aux sujets suivis par un utilisateur.
    """
    # Préparation : création d'un utilisateur et d'un sujet
    user_in = schemas.UserCreate(username="testuser", email="test@example.com", password="testpassword")
    user = crud.create_user(db_session, user=user_in)
    subject = crud.create_subject(db_session, subject_name="Python")

    # Test : ajout du sujet à l'utilisateur
    user = crud.add_subject_to_user(db_session, user=user, subject=subject)
    assert subject in user.liked_subjects

def test_remove_subject_from_user(db_session: Session):
    """
    Teste la suppression d'un sujet des sujets suivis par un utilisateur.
    """
    # Préparation : création d'un utilisateur et d'un sujet
    user_in = schemas.UserCreate(username="testuser", email="test@example.com", password="testpassword")
    user = crud.create_user(db_session, user=user_in)
    subject = crud.create_subject(db_session, subject_name="Django")

    # Ajout du sujet à l'utilisateur
    user = crud.add_subject_to_user(db_session, user=user, subject=subject)
    assert subject in user.liked_subjects

    # Test : suppression du sujet de l'utilisateur
    user = crud.remove_subject_from_user(db_session, user=user, subject=subject)
    assert subject not in user.liked_subjects

def test_create_article(db_session: Session):
    """
    Teste la création d'un nouvel article avec des sujets associés.
    """
    article_in = schemas.ArticleCreate(
        title="New in Python 3.10",
        summary="Details about the new features in Python 3.10.",
        published_at=datetime.utcnow(),
        url="https://example.com/python310",
        subjects=["Python"]
    )
    article = crud.create_article(db_session, article=article_in)
    assert article.title == "New in Python 3.10"
    assert len(article.subjects) == 1
    assert article.subjects[0].name == "Python"

def test_get_articles(db_session: Session):
    """
    Teste la récupération de la liste des articles.
    """
    # Préparation : création d'articles
    article_in1 = schemas.ArticleCreate(
        title="Article 1",
        summary="Summary 1",
        published_at=datetime.utcnow(),
        url="https://example.com/article1",
        subjects=["Subject1"]
    )
    article_in2 = schemas.ArticleCreate(
        title="Article 2",
        summary="Summary 2",
        published_at=datetime.utcnow(),
        url="https://example.com/article2",
        subjects=["Subject2"]
    )
    crud.create_article(db_session, article=article_in1)
    crud.create_article(db_session, article=article_in2)

    # Test
    articles = crud.get_articles(db_session)
    assert len(articles) == 2

def test_authenticate_user(db_session: Session):
    """
    Teste l'authentification d'un utilisateur avec un mot de passe correct et incorrect.
    """
    # Préparation : création d'un utilisateur
    user_in = schemas.UserCreate(username="testuser", email="test@example.com", password="testpassword")
    crud.create_user(db_session, user=user_in)

    # Test : authentification réussie
    user = crud.authenticate_user(db_session, username="testuser", password="testpassword")
    assert user is not False
    assert user.username == "testuser"

    # Test : échec d'authentification
    user = crud.authenticate_user(db_session, username="testuser", password="wrongpassword")
    assert user is False
