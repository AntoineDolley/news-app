from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class SubjectBase(BaseModel):
    name: str

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int

    class Config:
        orm_mode = True

class ArticleBase(BaseModel):
    title: str
    summary: str
    published_at: datetime
    url: str

class ArticleCreate(ArticleBase):
    subjects: List[str]

class Article(ArticleBase):
    id: int
    subjects: List[Subject] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    user_name: str

class UserCreate(UserBase):
    user_password: str

class User(UserBase):
    id: int
    liked_subjects: List[Subject] = []
    last_connection: datetime

    class Config:
        orm_mode = True
