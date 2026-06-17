from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    published_year = Column(Integer, nullable=False)
    cover_image_url = Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    author = relationship("Author", back_populates="books")
    category = relationship("Category", back_populates="books")
