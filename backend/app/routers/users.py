from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app import schemas, crud
from app.dependencies import get_db
from app.config import settings
from app.utils.auth import create_access_token

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    """
    Register a new user with a unique username and email.

    Parameters:
        user (schemas.UserCreate): The user data for registration, including username, password, and email.
        db (Session): The database session dependency.

    Returns:
        schemas.User: The newly created user with username, email, and other details.
    """
    db_user = crud.get_user_by_name(db, user_name=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà enregistré")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return crud.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> schemas.Token:
    """
    Authenticate a user and return an access token for API access.

    Parameters:
        form_data (OAuth2PasswordRequestForm): The login form data containing username and password.
        db (Session): The database session dependency.

    Returns:
        schemas.Token: A dictionary with the access token and token type.

    Raises:
        HTTPException: If the username or password is incorrect.
    """
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}