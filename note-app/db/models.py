from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class ModelBase(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)

class User(ModelBase):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    notes = relationship("Note", back_populates="user")
    category_user = relationship("Category", back_populates="user")

class Note(ModelBase):
    __tablename__ = "notes"

    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="notes")

    categories = relationship("CategoryNotes", back_populates="note")

class Category(ModelBase):
    __tablename__ = "categories"

    name = Column(String)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="category_user")

    notes = relationship("CategoryNotes", back_populates="category")

class CategoryNotes(ModelBase):
    __tablename__ = "category_notes"

    category_id = Column(Integer, ForeignKey("categories.id"))
    note_id = Column(Integer, ForeignKey("notes.id"))
    category = relationship("Category", back_populates="notes")
    note = relationship("Note", back_populates="categories")