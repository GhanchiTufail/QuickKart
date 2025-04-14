from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from source.config.database import Base, engine  # assuming you have a Base from database.py

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))  # assuming you have a products table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # optional if anonymous reviews allowed

    rating = Column(Integer, nullable=False)  # 1 to 5
    review_text = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Optional: relationships
    product = relationship("Product", back_populates="reviews")  # if defined in Product
    user = relationship("User", back_populates="reviews")  # if defined in User

Base.metadata.create_all(bind=engine)