from datetime import datetime
from enum import Enum
from sqlalchemy import Column, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Float, Boolean, DateTime, Text, JSON
from source.config.database import Base, engine

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")