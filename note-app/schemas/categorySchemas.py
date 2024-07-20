from pydantic import BaseModel
from . import noteSchemas

class CategoryBase(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

class AddNote(BaseModel):
    category: int
    note: int


    class Config:
        orm_mode = True