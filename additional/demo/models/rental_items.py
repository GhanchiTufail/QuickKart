from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, Float, Boolean, func
from sqlalchemy.orm import relationship
from source.config.database import Base, engine

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer,autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime)
    total_price = Column(Float) 
    status = Column(String(20), default="active")
    is_history = Column(Boolean)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="rentals")
    product = relationship("Product", back_populates="rentals")

Base.metadata.create_all(bind=engine)