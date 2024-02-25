from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.database import engine, SessionLocal
from database import models
from database.models import User, House
from database.users import BaseUser

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

@app.get("/users/", response_model=None)
async def read_users(db: SessionLocal = Depends(get_db)):
    return db.query(User).all()

@app.post("/create/", response_model=None)
async def create_user(user: BaseUser, db: SessionLocal = Depends(get_db)):
    model_user = User()
    model_user.username = user.username
    model_user.email = user.email
    db.add(model_user)
    db.commit()
    return user
