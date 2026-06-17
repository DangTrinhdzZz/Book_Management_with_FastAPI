from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import category, book, author, dependency

app = FastAPI(
    title = "Book Management API",
    description = "A simple API for managing books in a library.",
    version = "1.0.0"
)

#Include routers
app.include_router(category.router, prefix="/categories", tags=["Categories"])
app.include_router(book.router, prefix="/books", tags=["Books"])
app.include_router(author.router, prefix="/authors", tags=["Authors"])

#staticfile cho ảnh bìa


@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Management API!"}
