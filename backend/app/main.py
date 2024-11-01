from fastapi import FastAPI
from .routers import news, users, subjects

# Initialisation de l'application FastAPI
app = FastAPI(
    title="News Application API",
    description="Une API pour accéder aux dernières nouvelles et gérer les utilisateurs et leurs sujets suivis.",
    version="1.0.0"
)

# Inclusion des routeurs pour organiser les endpoints par fonctionnalité
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
