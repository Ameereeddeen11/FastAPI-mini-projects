from pydantic import BaseModel
from typing import Optional

class BaseHouse(BaseModel):
    address: str
    price: int
    owner: int

class House(BaseHouse):
    id: int
    class Config:
        orm_mode = True

class BaseUser(BaseModel):
    username: str
    email: str
    #house: int

class User(BaseUser):
    id: int
    class Config:
        orm_mode = True


'''class BaseUser(BaseModel):
    username: str
    email: str
    house: Optional[int]

class House(BaseModel):
    address: str
    price: int
    owner: Optional[int]'''