from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# URL de connexion à la base de données
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Création du moteur de base de données
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création de la session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles SQLAlchemy
Base = declarative_base()
