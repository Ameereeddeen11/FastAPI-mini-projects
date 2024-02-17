from fastapi import FastAPI, Path, Query, Depends
from enum import Enum
from models.user import User, UpdateUser
from typing import Annotated
from models.database import engine, SessionLocal
from models.models import Base
from sqlalchemy.orm import Session
from models import models

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

class DayName(int, Enum):
    Mondey = 1
    Tuesday = 2
    Wednesday = 3
    Thorusday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7

@app.get("/")
async def home():
    return {"message": "Hello World"}

# Path parameters
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/today/{day}")
async def day(day: DayName):
    match day:
        case DayName.Mondey:
            return {"day": "Monday"}
        case DayName.Tuesday:
            return {"day": "Tuesday"}
        case DayName.Wednesday:
            return {"day": "Wednesday"}
        case DayName.Thorusday:
            return {"day": "Thorusday"}
        case DayName.Friday:
            return {"day": "Friday"}
        case DayName.Saturday:
            return {"day": "Saturday"}
        case DayName.Sunday:
            return {"day": "Sunday"}
        case _:
            return {"day": "Invalid day"}

# Query parameters
@app.get("/query/")
async def query(item_id: int, day: DayName | None = None):
    if day:
        match day:
            case DayName.Mondey:
                return {"day": "Monday", "item_id": item_id}
            case DayName.Tuesday:
                return {"day": "Tuesday", "item_id": item_id}
            case DayName.Wednesday:
                return {"day": "Wednesday", "item_id": item_id}
            case DayName.Thorusday:
                return {"day": "Thorusday", "item_id": item_id}
            case DayName.Friday:
                return {"day": "Friday", "item_id": item_id}
            case DayName.Saturday:
                return {"day": "Saturday", "item_id": item_id}
            case DayName.Sunday:
                return {"day": "Sunday", "item_id": item_id}
            case _:
                return {"day": "Invalid day", "item_id": item_id}
    else:
        return {"item_id": item_id}

@app.get("/query2/{item_id}/{user}/")
async def query2(item_id: int, user: str, item: str = None, sold: bool = False):
    result = {"item_id": item_id, "user": user}
    if item:
        result.update({"item": item})
    if sold:
        result.update({"sold": sold})
    return result

users = {}

# Request body
# Request POST
@app.post("/createuser/{user_id}")
async def create_user(user: User, user_id: int):
    if user_id in users:
        return {"message": "User already exists"}
    users[user_id] = user
    return {"message": "User created"}

# Request GET
@app.get("/user/{user_id}")
async def read_user(user_id: int = Path(description="The ID of the user to read", gt=0), db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Request GET from database
@app.get("/user_all/")
async def read_user_all(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Request POST to database
@app.post("/createuser/")
async def create_user(user: User, db: Session = Depends(get_db)):
    book_model = models.User()
    book_model.name = user.name
    book_model.lastname = user.lastname
    book_model.age = user.age
    db.add(book_model)
    db.commit()
    return user

# Query parameters
"""@app.get("/user/")
async def user_name(name: Annotated[str | None, Query(max_length=50, gt=0)] = None):
    for data in users:
        if users[data].name == name:
            return users[data]
    return {"data": "User not found"}"""

# Request PUT
@app.put("/updateuser/{user_id}")
async def update_user(user: UpdateUser, user_id: int):
    if user_id not in users:
        return {"message": "User does not exist"}
    if user.name != None:
        users[user_id].name = user.name
    if user.lastname != None:
        users[user_id].lastname = user.lastname
    if user.age != None:
        users[user_id].age = user.age
    return {"message": "User updated"}