# tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.database import Base
from backend.app.dependencies import get_db

# Utiliser une base de données SQLite en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Créer un moteur de base de données pour les tests
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Créer une session de base de données pour les tests
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture pour la session de base de données
@pytest.fixture(scope="function")
def db_session():
    """
    Crée une nouvelle base de données pour chaque test et ferme la session après le test.
    """
    # Crée les tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Supprime les tables après le test
        Base.metadata.drop_all(bind=engine)
