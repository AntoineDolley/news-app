from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging
from ..database import SessionLocal
from ..utils.fetch_news import populate_function


logging.basicConfig(level=logging.INFO)

def scheduled_fetch_news():
    """
    Fonction qui sera appelée périodiquement pour récupérer et insérer les articles dans la DB.
    """
    logging.info(f"[SCHEDULER] Début de scheduled_fetch_news à {datetime.now()}")
    db = SessionLocal()
    try:
        # Appelez ici la fonction de peuplement que vous avez créée, par ex. main() ou fetch_and_populate_articles
        populate_function()
    except Exception as e:
        logging.error(f"[SCHEDULER] Erreur lors de la récupération des articles : {e}")
    finally:
        db.close()
    logging.info(f"[SCHEDULER] Fin de scheduled_fetch_news à {datetime.now()}")

def start_scheduler():
    """
    Configure et démarre l'APScheduler pour lancer 'scheduled_fetch_news' de temps en temps.
    """
    scheduler = BackgroundScheduler(timezone="UTC")
    # Exemple : run toutes les 6 heures
    scheduler.add_job(scheduled_fetch_news, IntervalTrigger(minutes=1), id='fetch_news_job')
    
    scheduler.start()
    logging.info("[SCHEDULER] APScheduler démarré.")
