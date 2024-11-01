from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str  # URL de connexion à la base de données PostgreSQL
    SECRET_KEY: str  # Clé secrète pour le chiffrement JWT
    ALGORITHM: str = "HS256"  # Algorithme de chiffrement pour JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Durée d'expiration du token JWT en minutes
    NEWS_API_KEY: str

    class Config:
        env_file = ".env"  # Chargement des variables d'environnement depuis un fichier .env

# Instanciation de la configuration globale
settings = Settings()
