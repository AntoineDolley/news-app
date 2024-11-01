from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# Association entre les utilisateurs et les sujets suivis (Many-to-Many)
user_subject = Table(
    'user_subject',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
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

    # Relation Many-to-Many avec User
    followers = relationship(
        'User',
        secondary=user_subject,
        back_populates='liked_subjects'
    )

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    summary = Column(String)
    published_at = Column(DateTime)
    url = Column(String)
    subjects = Column(String)  # Peut être modifié pour une relation avec Subject
