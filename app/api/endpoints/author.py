from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.api.endpoints.dependency import get_db
from app import model
from app.model.author import Author
from app.schema import Author
from app.schema.author import Author, AuthorCreate, AuthorUpdate
from sqlalchemy import Column, String

router = APIRouter()

@router.get("",response_model=List[Author]) 
def list_authors(
    skip : int = 0,
    limit : int = 100,
    db : Session = Depends(get_db)

):
    """Endpoint to retrieve a list of authors."""

    authors = db.query(model.Author).offset(skip).limit(limit).all()
    return authors

@router.get("", response_model=Author, status_code= status.HTTP_200_OK)
def get_author(
    author_id: int, 
    db: Session = Depends(get_db)
    ):
    author = db.query(model.Author).filter(model.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    return author

@router.post("", response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(
    author_in: AuthorCreate,
    db: Session = Depends(get_db)
):
    """Create new author. Check unique name and return the created author."""
    existing_author = db.query(model.Author).filter(model.Author.name == author_in.name).first()
    if existing_author:
        raise HTTPException(status_code=400, detail="Author with this name already exists")

    new_author = model.Author(name=author_in.name, biography=author_in.biography)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author

@router.put("", response_model=Author)
def update_author(
    author_id: int,
    author_in: AuthorUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing author. Check if the author exists and return the updated author."""
    author = db.query(model.Author).filter(model.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    if author_in.name is not None and author_in.name != author.name:
        existing_author = db.query(model.Author).filter(model.Author.name == author_in.name).first()
        if existing_author:
            raise HTTPException(status_code=400, detail="Author with this name already exists")
        author.name = author_in.name

    if author_in.biography is not None:
        author.biography = author_in.biography

    db.add(author)
    db.commit()
    db.refresh(author)

    return author

@router.delete("", response_model=Author)
def delete_Author(
    Author_id: int,
    db: Session = Depends(get_db)
):
    """Delete a Author by ID."""
    Author = db.query(model.Author).filter(model.Author.id == Author_id).first()
    if not Author:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(Author)
    db.commit()
    return Author
