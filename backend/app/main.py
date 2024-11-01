from fastapi import FastAPI
from backend.app.routers import news, users, subjects

# Initialisation de l'application FastAPI
app = FastAPI(
    title="News Application API",
    description="Une API pour accéder aux dernières nouvelles et gérer les utilisateurs et leurs sujets suivis.",
    version="1.0.0"
)

# Route de base pour vérifier l'état de l'API
@app.get("/")
async def root():
    """
    Endpoint de base pour vérifier que l'API est en ligne.

    Returns:
        dict: Message de bienvenue.
    """
    return {"message": "Bienvenue sur l'API de News App. L'API est en ligne."}

# Inclusion des routeurs pour organiser les endpoints par fonctionnalité
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
