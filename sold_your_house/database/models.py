from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)

    #house = relationship("House", back_populates="owner")

class House(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    price = Column(Integer, index=True)

    #owner = relationship("User", back_populates="house")