from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.types import UserDefinedType
from sqlalchemy import Float

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
    email = Column(String, unique=True, index=True)
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

class Vector(UserDefinedType):
    def get_col_spec(self):
        # Ajustez la dimension selon votre modèle (par ex. 1536 pour text-embedding-ada-002)
        return "vector(1536)"

class Article(Base):
    """
    Modèle pour les articles de news.

    Attributes:
        id (int): Identifiant unique de l'article.
        title (str): Titre de l'article.
        summary (str): Résumé de l'article. Peut être vide si non résumé.
        raw_text (str): Texte brut de l'article, tel qu'extrait de la source.
        published_at (DateTime): Date et heure de publication de l'article.
        url (str): URL de l'article complet.
        subjects (List[Subject]): Liste des sujets associés à l'article.
    """
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)  # Peut être NULL
    raw_text = Column(Text, nullable=False)  # Stocke le texte brut
    published_at = Column(DateTime, nullable=False)
    url = Column(String, unique=True, index=True, nullable=False)
    embedding = Column(Vector)
    subjects = relationship(
        'Subject',
        secondary=article_subject_association,
        back_populates='articles'
    )
    __table_args__ = (
        UniqueConstraint('url', name='unique_article_url'),
    )