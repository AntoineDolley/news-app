from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Table d'association entre les utilisateurs et les sujets
user_subject_association = Table(
    'user_subject', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)

# Table d'association entre les articles et les sujets
article_subject_association = Table(
    'article_subject', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    user_password = Column(String)
    last_connection = Column(DateTime)
    liked_subjects = relationship(
        'Subject',
        secondary=user_subject_association,
        back_populates='users'
    )

class Subject(Base):
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
