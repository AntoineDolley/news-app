from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class SubjectBase(BaseModel):
    """
    Schéma de base pour un sujet suivi ou associé à des articles.

    Attributes:
        name (str): Nom du sujet.
    """
    name: str

class SubjectCreate(SubjectBase):
    """
    Schéma pour la création d'un sujet, basé sur SubjectBase.
    """
    pass

class Subject(SubjectBase):
    """
    Schéma de réponse pour un sujet, incluant son identifiant.

    Attributes:
        id (int): Identifiant unique du sujet.
    """
    id: int

    class Config:
        orm_mode = True  # Active la compatibilité avec SQLAlchemy


class ArticleBase(BaseModel):
    """
    Schéma de base pour un article de news.

    Attributes:
        title (str): Titre de l'article.
        summary (str): Résumé de l'article.
        published_at (datetime): Date et heure de publication de l'article.
        url (str): URL de l'article complet.
    """
    title: str
    raw_text: str
    published_at: datetime
    url: str


class ArticleCreate(ArticleBase):
    """
    Schéma pour la création d'un article, incluant les sujets associés.

    Attributes:
        subjects (List[str]): Liste des noms des sujets associés à l'article.
    """
    summary: Optional[str] = None

class Article(ArticleBase):
    """
    Schéma de réponse pour un article, incluant les sujets associés.

    Attributes:
        id (int): Identifiant unique de l'article.
        subjects (List[Subject]): Liste des sujets associés à l'article.
    """
    id: int
    summary: Optional[str] = None

    class Config:
        orm_mode = True  # Active la compatibilité avec SQLAlchemy


class UserBase(BaseModel):
    """
    Schéma de base pour un utilisateur de l'application.

    Attributes:
        user_name (str): Nom d'utilisateur unique.
        email (EmailStr): Adresse e-mail de l'utilisateur.
    """
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """
    Schéma pour la création d'un utilisateur, incluant le mot de passe en clair.

    Attributes:
        user_password (str): Mot de passe de l'utilisateur.
    """
    password: str

class User(UserBase):
    """
    Schéma de réponse pour un utilisateur, incluant les sujets suivis et la dernière connexion.

    Attributes:
        id (int): Identifiant unique de l'utilisateur.
        liked_subjects (List[Subject]): Liste des sujets suivis par l'utilisateur.
        last_connection (datetime): Date et heure de la dernière connexion de l'utilisateur.
    """
    id: int
    liked_subjects: List[Subject] = []
    last_connection: datetime

    class Config:
        orm_mode = True  # Active la compatibilité avec SQLAlchemy

class Token(BaseModel):
    """
    Schéma pour le token d'authentification renvoyé par l'API lors de la connexion.

    Attributes:
        access_token (str): Le token JWT d'accès.
        token_type (str): Le type de token (par ex., "bearer").
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schéma pour stocker les données du token d'authentification.

    Attributes:
        username (Optional[str]): Nom d'utilisateur extrait du token JWT.
    """
    username: Optional[str] = None