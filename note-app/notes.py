from fastapi import APIRouter, Depends, UploadFile, File, Form
from db.db import SessionLocal
from typing import Annotated, List
from db.models import *
from auth import get_current_user
from schemas.noteSchemas import *
from PIL import Image
from io import BytesIO
import datetime, os
from sqlalchemy.orm import Session

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
async def create_note(
        title: str = Form(...),
        content: str = Form(...),
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
        files: List[UploadFile] = File(...),
):
    note = NoteSchema(title=title, content=content)
    new_note = await create_notes(db=db, note=note, user=user)
    for file in files:
        image_path = f"images/{file.filename}"
        with open(image_path, "wb") as buffer:
            buffer.write(file.file.read())
        new_image = ImageNote(
            url=image_path,
            note_id=new_note.id
        )
    return new_note

async def create_notes(
        note: NoteSchema,
        db: db_dependency,
        user: user_dependency
        # image_path: str
):
    new_note = Note(
        title=note.title,
        content=note.content,
        created_at=datetime.datetime.now(),
        user_id=user["user_id"]
    )
    db.add(new_note)
    db.commit()

    # new_image = ImageNote(
    #     url=image_path,
    #     note_id=new_note.id
    # )
    # db.add(new_image)
    # db.commit()

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