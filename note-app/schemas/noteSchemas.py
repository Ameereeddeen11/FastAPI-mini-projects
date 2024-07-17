from pydantic import BaseModel

class NoteSchema(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True
