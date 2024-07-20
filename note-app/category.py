from fastapi import APIRouter, Depends
from db.db import SessionLocal
from typing import Annotated
from db.models import *
from auth import get_current_user
from schemas.categorySchemas import *

router = APIRouter(
    prefix="/category",
    tags=["category"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=200)
async def get_category(db: db_dependency, user: user_dependency):
    if not user:
        return {"message": "No user found"}
    get_category = db.query(Category).filter(user["user_id"] == Category.user_id).all()
    if not get_category:
        return {"message": "No category found"}
    return get_category

@router.get("/{category_id}", status_code=200)
async def get_category_by_id(category_id: int, db: db_dependency, user: user_dependency):
    if not user:
        return {"message": "No user found"}
    category = db.query(CategoryNotes).filter(category_id == CategoryNotes.id).first()
    note = db.query(Note).filter(category.note_id == Note.id).first()
    user = db.query(User).filter(note.user_id == user["user_id"]).first()
    if not user:
        return {"message": "No user found"}
    if not category:
        return {"message": "Category not found"}
    return category

@router.post("/create", status_code=201)
async def create_category(category: CategoryBase, db: db_dependency, user: user_dependency):
    if not user:
        return {"message": "No user found"}
    new_category = Category(
        name=category.name,
        description=category.description,
        user_id=user["user_id"]
    )
    db.add(new_category)
    db.commit()

    return new_category

@router.post("/add-note", status_code=201)
async def add_note_to_category(add_note: AddNote, db: db_dependency, user: user_dependency):
    if not user:
        return {"message": "No user found"}
    category = db.query(Category).filter(add_note.category == Category.id, user["user_id"] == Category.user_id).first()
    if not category:
        return {"message": "Category not found"}
    note = db.query(Note).filter(add_note.note == Note.id, user["user_id"] == Note.user_id).first()
    if not note:
        return {"message": "Note not found"}
    category_note = CategoryNotes(
        category_id=category.id,
        note_id=note.id
    )
    db.add(category_note)
    db.commit()

    return category_note

