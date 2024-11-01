from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_user_by_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()

def create_user(db: Session, user: schemas.UserCreate):
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

def get_subject_by_name(db: Session, subject_name: str):
    return db.query(models.Subject).filter(models.Subject.name == subject_name).first()

def create_subject(db: Session, subject_name: str):
    db_subject = models.Subject(name=subject_name)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def add_subject_to_user(db: Session, user: models.User, subject: models.Subject):
    if subject not in user.liked_subjects:
        user.liked_subjects.append(subject)
        db.commit()
        db.refresh(user)
    return user

def remove_subject_from_user(db: Session, user: models.User, subject: models.Subject):
    if subject in user.liked_subjects:
        user.liked_subjects.remove(subject)
        db.commit()
        db.refresh(user)
    return user

def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()

def get_article_by_id(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(
        title=article.title,
        summary=article.summary,
        published_at=article.published_at,
        url=article.url
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    # Ajout des sujets associés
    for subject_name in article.subjects:
        subject = get_subject_by_name(db, subject_name)
        if not subject:
            subject = create_subject(db, subject_name)
        db_article.subjects.append(subject)
    db.commit()
    db.refresh(db_article)
    return db_article

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_name(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user