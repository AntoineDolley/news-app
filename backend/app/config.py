from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str  # Clé secrète pour le chiffrement JWT
    ALGORITHM: str = "HS256"  # Algorithme de chiffrement pour JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300000  # Durée d'expiration du token JWT en minutes
    NEWS_API_KEY: str
    OPENAI_API_KEY: str # Clé API OpenAI

    class Config:
        env_file = ".env"  # Chargement des variables d'environnement depuis un fichier .env

# Instanciation de la configuration globale
settings = Settings()
