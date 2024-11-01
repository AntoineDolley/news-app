from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# URL de connexion à la base de données
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Création du moteur de base de données pour PostgreSQL
# `create_engine` établit la connexion avec les paramètres fournis dans SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création de la session locale
# `sessionmaker` configure les sessions pour les transactions de base de données,
# avec autocommit et autoflush désactivés pour un contrôle explicite des transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles SQLAlchemy
# `declarative_base` sert de base pour la définition des modèles
Base = declarative_base()
