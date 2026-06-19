from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schema.author import Author
from app.schema.category import Category

class BookBase(BaseModel):
    title   : str
    description: str | None = None
    published_year : int | None = None
    category_id : int | None = None
    author_id : int | None = None

class BookCreate(BookBase):
    """Schema for creating a new Book."""
    pass
    
class BookUpdate(BaseModel):
    """Schema for updating an existing Book."""
    title   : str | None = None
    description: str | None = None
    published_year : int | None = None
    category_id : int | None = None
    author_id : int | None = None

class BookInDBBase(BookBase):
    """Schema for Book data stored in the database."""
    id: int
    title : str
    description : str | None = None
    published_year : int | None = None
    category_id : int | None = None
    author_id : int | None = None
    cover_image_url : str | None = None
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True # Pydantic  read from SQLAlchemy models

class Book(BookInDBBase):
    """Schema for Book data returned in API responses."""
    author :Author
    category : Category
