from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.api.endpoints.dependency import get_db
from app import model
from app.schema.category import Category, CategoryCreate, CategoryUpdate
from sqlalchemy import Column, String


router = APIRouter()

@router.get("",response_model=List[Category]) 
def list_categories(
    skip : int = 0,
    limit : int = 100,
    db : Session = Depends(get_db)

):
    """Endpoint to retrieve a list of categories."""

    categories = db.query(model.Category).offset(skip).limit(limit).all()
    return categories

@router.get("", response_model=Category, status_code= status.HTTP_200_OK)
def get_category(
    category_id: int, 
    db: Session = Depends(get_db)
    ):
    category = db.query(model.Category).filter(model.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category

@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db)
):
    """Create new category. Check unique name and return the created category."""
    existing_category = db.query(model.Category).filter(model.Category.name == category_in.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    desciption = category_in.description if category_in.description is not None else ""
    new_category = model.Category(name=category_in.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category

@router.put("", response_model=Category)
def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing category. Check if the category exists and return the updated category."""
    category = db.query(model.Category).filter(model.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category_in.name is not None and category_in.name != category.name:
        existing_category = db.query(model.Category).filter(model.Category.name == category_in.name).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
        category.name = category_in.name

    if category_in.description is not None:
        category.description = category_in.description

    db.add(category)
    db.commit()
    db.refresh(category)
    
    return category

@router.delete("", response_model=Category)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Delete a category by ID."""
    category = db.query(model.Category).filter(model.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return category
