from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str
    biography: str | None = None

class AuthorCreate(AuthorBase):
    """Schema for creating a new Author."""
    pass
    
class AuthorUpdate(BaseModel):
    """Schema for updating an existing Author."""
    name : str | None = None
    description : str | None = None

class AuthorInDBBase(AuthorBase):
    """Schema for Author data stored in the database."""
    id: int

    class Config:
        orm_mode = True # Pydantic  read from SQLAlchemy models

class Author(AuthorInDBBase):
    """Schema for Author data returned in API responses."""
    pass