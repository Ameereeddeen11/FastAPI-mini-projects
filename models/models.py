from sqlalchemy import String, Integer, Column
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lastname = Column(String)
    age = Column(Integer)

