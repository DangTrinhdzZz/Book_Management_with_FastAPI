from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None
class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    pass
    
class CategoryUpdate(BaseModel):
    """Schema for updating an existing category."""
    name : str | None = None
    description : str | None = None

class CategoryInDBBase(CategoryBase):
    """Schema for category data stored in the database."""
    id: int

    class Config:
        orm_mode = True # Pydantic  read from SQLAlchemy models

class Category(CategoryInDBBase):
    """Schema for category data returned in API responses."""
    pass