from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str
    notes: list

    class Config:
        orm_mode = True

