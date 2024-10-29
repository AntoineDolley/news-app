from fastapi import FastAPI, Depends
from . import models, schemas, crud, database
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/news/")
def read_news():
    return {"message": "This is the news API"}
