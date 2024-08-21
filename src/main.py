from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from database import engine, get_db


# Create models if not exist
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def hello():
    return {"Hello": "World"}
