from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from backend.app.database import Base

# Table d'association entre les utilisateurs et les sujets
user_subject_association = Table(
    'user_subject', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)
"""
Table d'association pour gérer la relation plusieurs-à-plusieurs entre les utilisateurs et les sujets.
"""

# Table d'association entre les articles et les sujets
article_subject_association = Table(
    'article_subject', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)
"""
Table d'association pour gérer la relation plusieurs-à-plusieurs entre les articles et les sujets.
"""

class User(Base):
    """
    Modèle pour les utilisateurs de l'application.

    Attributes:
        id (int): Identifiant unique de l'utilisateur.
        username (str): Nom d'utilisateur unique.
        hashed_password (str): Mot de passe haché de l'utilisateur.
        last_connection (DateTime): Dernière date de connexion de l'utilisateur.
        liked_subjects (List[Subject]): Liste des sujets suivis par l'utilisateur.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    last_connection = Column(DateTime)
    liked_subjects = relationship(
        'Subject',
        secondary=user_subject_association,
        back_populates='users'
    )


class Subject(Base):
    """
    Modèle pour les sujets suivis par les utilisateurs et associés aux articles.

    Attributes:
        id (int): Identifiant unique du sujet.
        name (str): Nom du sujet.
        users (List[User]): Liste des utilisateurs suivant ce sujet.
        articles (List[Article]): Liste des articles associés à ce sujet.
    """
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    users = relationship(
        'User',
        secondary=user_subject_association,
        back_populates='liked_subjects'
    )
    articles = relationship(
        'Article',
        secondary=article_subject_association,
        back_populates='subjects'
    )


class Article(Base):
    """
    Modèle pour les articles de news.

    Attributes:
        id (int): Identifiant unique de l'article.
        title (str): Titre de l'article.
        summary (str): Résumé de l'article.
        published_at (DateTime): Date et heure de publication de l'article.
        url (str): URL de l'article complet.
        subjects (List[Subject]): Liste des sujets associés à l'article.
    """
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    summary = Column(String)
    published_at = Column(DateTime)
    url = Column(String)
    subjects = relationship(
        'Subject',
        secondary=article_subject_association,
        back_populates='articles'
    )
