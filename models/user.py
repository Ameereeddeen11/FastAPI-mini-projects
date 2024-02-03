from pydantic import BaseModel
from typing import Optional

# Data model for the user
class User(BaseModel):
    id: int
    name: str
    lastname: str | None = None
    age: int

# Data model for updating the user
class UpdateUser(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None
