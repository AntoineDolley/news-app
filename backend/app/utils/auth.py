from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
from app.config import settings

# Initialisation du contexte pour le hachage de mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Parameters:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that a plain text password matches its hashed version.

    Parameters:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Create a JSON Web Token (JWT) for a given set of data.

    Parameters:
        data (dict): The data to include in the token payload, typically {"sub": username}.
        expires_delta (Union[timedelta, None]): Optional expiration time for the token.
            If not provided, the default expiration time from settings is used.

    Returns:
        str: The encoded JWT as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
