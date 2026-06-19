from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, Query, File 
from typing import List
from sqlalchemy.orm import Session

from app.api.endpoints.dependency import get_db
from app import model
from app.schema.book import Book, BookCreate, BookUpdate
from app.schema.category import Category, CategoryCreate, CategoryUpdate
from sqlalchemy import Column, String, or_
from pathlib import Path
import uuid

#folder save cover image
UPLOAD_DIR = Path("app/static/covers")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

@router.get("/", response_model=List[Book]) 
def list_books(
    db : Session = Depends(get_db),
    skip : int = 0,
    limit : int = 100,
    author_id : int | None = Query(None),
    year : int | None = Query(None),
    keyword : str | None = Query(None)
):
    "Get list of books with optional filters for author, published year, and keyword in title or description."
    query = db.query(model.Book)
    if author_id is not None:
        query = query.filter(model.Book.author_id == author_id)
    if year is not None:
        query = query.filter(model.Book.year == year)
    if keyword is not None:
        like_pattern = f"%{keyword}%"
        query = query.filter(or_(model.Book.title.ilike(like_pattern), model.Book.description.ilike(like_pattern)))
    books = query.offset(skip).limit(limit).all()
    return {"message": "List of books", "books": books}

@router.get("/{book_id}", response_model=Book, status_code= status.HTTP_200_OK)
def get_book(
    book_id: int, 
    db: Session = Depends(get_db)
    ):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book

@router.post("", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: BookCreate,
    db: Session = Depends(get_db)
):
    """Create new book. Check unique name and return the created book."""
    author_id = db.query(model.Author.id).filter(model.Author.id == book_in.author_id).scalar()
    if not author_id:
        raise HTTPException(status_code=400, detail="Author not found")
    category_id = db.query(model.Category.id).filter(model.Category.id == book_in.category_id).scalar()
    if not category_id:
        raise HTTPException(status_code=400, detail="Category not found")
    existing_book = db.query(model.Book).filter(model.Book.name == book_in.name).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book with this name already exists")

    description = book_in.description if book_in.description is not None else ""
    new_book = model.Category(name=book_in.name, description=description, year=book_in.year, author_id=author_id, category_id=category_id)  
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book_in: BookUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing book. Check if the book exists and return the updated book."""
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.title is not None and book_in.title != book.title:
        existing_book = db.query(model.Book).filter(model.Book.title == book_in.title).first()
        if existing_book:
            raise HTTPException(status_code=400, detail="Book with this title already exists")
        book.title = book_in.title
    if book_in.published_year is not None:
        book.published_year = book_in.published_year
    if book_in.category_id is not None:
        category_id = db.query(model.Category.id).filter(model.Category.id == book_in.category_id).scalar()
        if not category_id:
            raise HTTPException(status_code=400, detail="Category not found")
        book.category_id = book_in.category_id
    if book_in.author_id is not None:
        author_id = db.query(model.Author.id).filter(model.Author.id == book_in.author_id).scalar()
        if not author_id:
            raise HTTPException(status_code=400, detail="Author not found")
        book.author_id = book_in.author_id 

    if book_in.description is not None:
        book.description = book_in.description

    db.add(book)
    db.commit()
    db.refresh(book)

    return book

@router.delete("/{book_id}", response_model=Book)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
                ):
    """Delete a Book by ID."""
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return book


@router.post("/{book_id}/cover", response_model=Book)
async def upload_cover_image(
    book_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload cover image for a book."""
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

    #Get extension of file
    extension = file.Path(file.filename).suffix.lower()
    if extension not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="Invalid file extension. Only .jpg, .jpeg, and .png are allowed.")
    #Read content file 
    content = await file.read()
    max_size = 2 * 1024 * 1024  # 2MB
    if len(content) > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 2MB.")


    # Save the uploaded file
    filename = f"{uuid.uuid4()}.jpg"
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as f:
        f.write(content)

    # Update the book's cover image URL
    book.cover_image_url = f"/static/covers/{filename}"
    db.add(book)
    db.commit()
    db.refresh(book)

    return book