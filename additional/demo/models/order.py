from datetime import datetime
from enum import Enum
from sqlalchemy import Column, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Float, Boolean, DateTime, Text, JSON
from ..config.database import Base, engine
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float, nullable=False)
    status = Column(String, default="Pending")  # Pending, Confirmed, Canceled
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

Base.metadata.create_all(bind=engine)