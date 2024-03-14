from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.database import engine, SessionLocal
from typing import Annotated
from database import models
from database.models import User, House
from database.schemas import BaseUser

app = FastAPI()

template = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return template.TemplateResponse("main.html", {"request": request})

@app.get("/users/", response_model=list[BaseUser])
async def read_users(db: SessionLocal = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_name}", response_model=BaseUser)
async def read_users(user_name: str, db: SessionLocal = Depends(get_db)):
    if db.query(User).filter(User.username == user_name).first():
        return db.query(User).filter(User.username == user_name).first()
    else:
        return {"error": "User not found"}

@app.post("/create/", response_model=None)
async def create_user(user: BaseUser, db: SessionLocal = Depends(get_db)):
    model_user = User()
    model_user.username = user.username
    model_user.email = user.email
    db.add(model_user)
    db.commit()
    return user
