from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app import schemas, models, crud
from app.database import SessionLocal
from app.config import settings

def get_db() -> Session:
    """
    Generate a database session for dependency injection.

    Yields:
        Session: A SQLAlchemy database session.

    Ensures:
        The session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2PasswordBearer scheme
# This dependency retrieves the token from the request Authorization header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """
    Retrieve the current user based on the provided JWT token.

    Parameters:
        token (str): The JWT token from the Authorization header.
        db (Session): The database session dependency.

    Returns:
        models.User: The authenticated user object.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token to retrieve the username
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # Retrieve the user from the database
    user = crud.get_user_by_name(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
