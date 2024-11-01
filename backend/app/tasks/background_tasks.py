from sqlalchemy.orm import Session
from ..utils.fetch_news import fetch_news
from .. import crud, models, schemas
from datetime import datetime

def check_for_updates(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        for subject in user.liked_subjects:
            articles_data = fetch_news(subject.name)
            for article_data in articles_data:
                article_create = schemas.ArticleCreate(**article_data)
                existing_article = db.query(models.Article).filter(models.Article.url == article_create.url).first()
                if not existing_article:
                    crud.create_article(db, article_create)
        user.last_connection = datetime.utcnow()
        db.commit()
