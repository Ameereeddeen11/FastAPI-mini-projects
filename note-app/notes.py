from fastapi import APIRouter, Depends
from db.db import SessionLocal
from typing import Annotated
from db.models import *
from auth import get_current_user
from schemas.noteSchemas import *
import datetime

router = APIRouter(
    prefix="/note",
    tags=["note"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/note/{note_id}")
async def get_note(note_id: int, db: db_dependency, user: user_dependency):
    note = db.query(Note).filter(note_id == Note.id, user["user_id"] == Note.user_id).first()
    if not note:
        return {"message": "Note not found"}
    return note

@router.post("/create", status_code=201)
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

@router.put("/update/{note_id}", status_code=200)
async def update_note(note_id: int, note: NoteSchema, db: db_dependency, user: user_dependency):
    note_to_update = db.query(Note).filter(note_id == Note.id, user["user_id"] == Note.user_id).first()
    if not note_to_update:
        return {"message": "Note not found"}
    note_to_update.title = note.title
    note_to_update.content = note.content
    db.commit()

    return note_to_update

@router.delete("/delete/{note_id}", status_code=200)
async def delete_note(note_id: int, db: db_dependency, user: user_dependency):
    note_to_delete = db.query(Note).filter(note_id == Note.id, user["user_id"] == Note.user_id).first()
    if not note_to_delete:
        return {"message": "Note not found"}
    db.delete(note_to_delete)
    db.commit()

    return {"message": "Note deleted"}