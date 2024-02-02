from fastapi import FastAPI
from enum import Enum

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
            return {"day": "Mondey"}
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