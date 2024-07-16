from fastapi import FastAPI, Depends
from db.db import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Annotated
from db.models import *

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def home():
    return {"message": "Hello World"}