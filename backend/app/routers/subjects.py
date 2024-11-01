from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter()

@router.post("/subjects/follow", response_model=schemas.User)
def follow_subject(user_name: str, subject_name: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_name(db, user_name=user_name)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    subject = crud.get_subject_by_name(db, subject_name=subject_name)
    if not subject:
        subject = crud.create_subject(db, subject_name=subject_name)
    user = crud.add_subject_to_user(db, user, subject)
    return user

@router.delete("/subjects/follow", response_model=schemas.User)
def unfollow_subject(user_name: str, subject_name: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_name(db, user_name=user_name)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    subject = crud.get_subject_by_name(db, subject_name=subject_name)
    if not subject:
        raise HTTPException(status_code=404, detail="Sujet non trouvé")
    user = crud.remove_subject_from_user(db, user, subject)
    return user

@router.get("/subjects/followed", response_model=List[schemas.Subject])
def get_followed_subjects(user_name: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_name(db, user_name=user_name)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user.liked_subjects
