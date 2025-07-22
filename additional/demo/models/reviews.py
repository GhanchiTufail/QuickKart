from sqlalchemy import Column, Integer, Text, DateTime, func
from sqlalchemy.orm import relationship
from source.config.database import Base,engine

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)  # assuming you have a products table
    user_id = Column(Integer)  # optional if anonymous reviews allowed
    rating = Column(Integer, nullable=False)  # 1 to 5
    review_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())

Base.metadata.create_all(bind=engine)