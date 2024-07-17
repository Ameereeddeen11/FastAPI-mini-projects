from fastapi import FastAPI, Depends
from db.db import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Annotated
from db.models import *
from auth import get_current_user
from schemas.noteSchemas import *
import auth, datetime

app = FastAPI()
app.include_router(auth.router)

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

@app.get("/note/{note_id}")
async def get_note(note_id: int, db: db_dependency, user: user_dependency):
    note = db.query(Note).filter(note_id == Note.id, user["user_id"] == Note.user_id).first()
    if not note:
        return {"message": "Note not found"}
    return note

@app.post("/create")
async def create_note(note: NoteSchema, db: db_dependency, user: user_dependency):
    new_note = Note(
        title=note.title,
        content=note.content,
        created_at=datetime.datetime.now(),
        user_id=user["user_id"]
    )
    db.add(new_note)
    db.commit()

    return new_note

@app.put("/update/{note_id}")
async def update_note(note_id: int, note: NoteSchema, db: db_dependency, user: user_dependency):
    note_to_update = db.query(Note).filter(note_id == Note.id, user["user_id"] == Note.user_id).first()
    if not note_to_update:
        return {"message": "Note not found"}
    note_to_update.title = note.title
    note_to_update.content = note.content
    db.commit()

    return note_to_update

@app.delete("/delete/{note_id}")
async def delete_note(note_id: int, db: db_dependency, user: user_dependency):
    note_to_delete = db.query(Note).filter(note_id == Note.id, user["user_id"] == Note.user_id).first()
    if not note_to_delete:
        return {"message": "Note not found"}
    db.delete(note_to_delete)
    db.commit()

    return {"message": "Note deleted"}