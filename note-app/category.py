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

@router.get("caterogry/", status_code=200)
async def get_category(db: db_dependency, user: user_dependency):
    if not user:
        return {"message": "No user found"}
    get_category = db.query(Category).filter(user["user_id"] == Category.notes.user_id).all()
    if not get_category:
        return {"message": "No category found"}
    return get_category

@router.get("/category/{category_id}", status_code=200)
async def get_category_by_id(category_id: int, db: db_dependency, user: user_dependency):
    if not user:
        return {"message": "No user found"}
    category = db.query(Category).filter(category_id == Category.id, user["user_id"] == Category.notes.user_id).first()
    if not category:
        return {"message": "Category not found"}
    return category

@router.post("/create", status_code=201)
async def create_category(category: CategoryBase, db: db_dependency, user: user_dependency):
    if not user:
        return {"message": "No user found"}
    notes_list = db.query(Note).filter(category.notes == Note.id).all()
    if user["user_id"] == notes_list.user_id:
        return {"message": "User not authorized to create category"}
    new_category = Category(
        name=category.name,
        user_id=user["user_id"]
    )
    db.add(new_category)
    db.commit()

    return new_category