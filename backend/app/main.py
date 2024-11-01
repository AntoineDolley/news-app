from fastapi import FastAPI
from .routers import news, users, subjects

app = FastAPI()

# Inclusion des routeurs
app.include_router(news.router)
app.include_router(users.router)
app.include_router(subjects.router)
