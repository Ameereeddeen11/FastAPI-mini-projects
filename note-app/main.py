from fastapi import FastAPI, Depends
from db.db import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Annotated
from db.models import *
from auth import get_current_user
import auth, notes, category

app = FastAPI()
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(category.router)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/")
async def home(db: db_dependency, user: user_dependency):
    if user is None:
        return {"message": "No user found"}
    notes = db.query(Note).filter(Note.user_id == user["user_id"]).all()
    if not notes:
        return {"message": "No notes found"}
    return notes
