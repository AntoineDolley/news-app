from sqlalchemy.orm import Session
from app.utils.fetch_news import fetch_news_by_keyword
from app import crud, models, schemas
from datetime import datetime

def check_for_updates(user_id: int, db: Session) -> None:
    """
    Check for new articles related to the subjects followed by a specific user and update their last connection.

    This function fetches the latest articles for each subject followed by the user.
    If a new article is found (an article not already stored in the database), it is added.
    Finally, the user's `last_connection` timestamp is updated to the current time.

    Parameters:
        user_id (int): The ID of the user whose followed subjects are being checked for updates.
        db (Session): The database session used for querying and updating the database.

    Returns:
        None

    Raises:
        None, but the function commits updates to the database.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        for subject in user.liked_subjects:
            # Fetch latest articles related to the subject's name
            articles_data = fetch_news_by_keyword(subject.name)
            for article_data in articles_data:
                # Create an ArticleCreate schema from the fetched data
                article_create = schemas.ArticleCreate(**article_data)
                # Check if the article already exists in the database by URL
                existing_article = db.query(models.Article).filter(models.Article.url == article_create.url).first()
                # If the article does not exist, add it to the database
                if not existing_article:
                    crud.create_article(db, article_create)
        # Update the user's last connection time to the current time
        user.last_connection = datetime.utcnow()
        db.commit()

