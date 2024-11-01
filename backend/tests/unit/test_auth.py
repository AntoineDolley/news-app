# tests/unit/test_auth.py

from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.config import settings
from datetime import timedelta, datetime
import time
from jose import jwt

def test_get_password_hash():
    """
    Teste le hachage d'un mot de passe.
    """
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert hashed_password.startswith("$2b$")  # Vérifie que bcrypt est utilisé

def test_verify_password():
    """
    Teste la vérification d'un mot de passe en clair avec son hachage.
    """
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False

def test_create_access_token():
    """
    Teste la création d'un token JWT et sa validité.
    """
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=1)
    token = create_access_token(data=data, expires_delta=expires_delta)
    assert token is not None

    # Décodage du token pour vérifier le contenu
    decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded_data["sub"] == "testuser"

    # Vérification de l'expiration du token
    expiration = datetime.utcfromtimestamp(decoded_data.get("exp"))
    assert expiration > datetime.utcnow()
