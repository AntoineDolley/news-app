from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.news import router as news_router
from .routers.users import router as users_router
from .routers.subjects import router as subjects_router
from .tasks.background_tasks import start_scheduler

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialisation de l'application FastAPI
app = FastAPI(
    title="News Application API",
    description="Une API pour accéder aux dernières nouvelles et gérer les utilisateurs et leurs sujets suivis.",
    version="1.0.0"
)

start_scheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Autoriser les requêtes depuis le frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

print("ajout des routes")
app.include_router(news_router, prefix="/news", tags=["News"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(subjects_router, prefix="/subjects", tags=["Subjects"])
