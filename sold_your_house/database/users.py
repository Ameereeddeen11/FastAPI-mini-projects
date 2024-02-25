from pydantic import BaseModel
from typing import Optional

class BaseUser(BaseModel):
    username: str
    email: str
    #house: int

class House(BaseModel):
    address: str
    price: int
    owner: int