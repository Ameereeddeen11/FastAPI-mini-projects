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
    get_category_note = db.query(CategoryNotes).filter(CategoryNotes.category_id == get_category.id)
    if not get_category and not get_category_note:
        return {"message": "No category found"}
    return get_category, get_category_note

@router.get("/{category_id}", status_code=200)
async def get_category_by_id(category_id: int, db: db_dependency, user: user_dependency):
    if not user:
        return {"message": "No user found"}
    category = db.query(CategoryNotes).filter(category_id == CategoryNotes.id).first()
    get_category_note = db.query(CategoryNotes).filter(category.id == CategoryNotes.category_id)
    note = db.query(Note).filter(category.note_id == Note.id).first()
    user_note= db.query(User).filter(note.user_id == user["user_id"]).first()
    if not user_note:
        return {"message": "No user found"}
    if not category and not get_category_note:
        return {"message": "Category not found"}
    return category, get_category_note

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

@router.delete("/{category_id}", status_code=200)
async def delete_category(category_id: int, db: db_dependency, user: user_dependency):
    if not user:
        return {"message": "No user found"}
    category = db.query(Category).filter(category_id == Category.id, user["user_id"] == Category.user_id).first()
    if not category:
        return {"message": "Category not found"}
    db.delete(category)
    db.commit()

    return {"message": "Category deleted"}

@router.delete("/{category_id}/{remove_note}", status_code=200)
async def remove_note_from_category(remove_note: int, category_id: int, db: db_dependency, user: user_dependency):
    if not user:
        return {"message": "No user found"}
    note = db.query(CategoryNotes).filter(remove_note == CategoryNotes.note_id, category_id == CategoryNotes.category_id).first()
    if not note:
        return {"message": "Note not found"}
    db.delete(note)
    db.commit()

    return {"message": "Note removed from category"}
