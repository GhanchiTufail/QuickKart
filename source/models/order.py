# from datetime import datetime
# from enum import Enum
# from sqlalchemy import Column, ForeignKey, Index, UniqueConstraint
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.sqltypes import (
#     Integer, String, Float, Boolean, DateTime, Text, JSON
# )
# from ..config.database import Base

# # Enums for status fields
# class OrderStatus(str, Enum):
#     PLACED = "placed"
#     SHIPPED = "shipped"
#     DELIVERED = "delivered"
#     CANCELLED = "cancelled"

# class PaymentStatus(str, Enum):
#     PENDING = "pending"
#     SUCCESS = "success"
#     FAILED = "failed"

# class TicketStatus(str, Enum):
#     OPEN = "open"
#     IN_PROGRESS = "in_progress"
#     CLOSED = "closed"

# # Order Management
# class Order(Base):
#     __tablename__ = "orders"
    
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     total = Column(Float, nullable=False)
#     status = Column(String(20), default=OrderStatus.PLACED)
#     shipping_address_id = Column(Integer, ForeignKey("addresses.id"))
#     payment_method = Column(String(50))
#     created_at = Column(DateTime, default=datetime.utcnow)
    
#     user = relationship("User", back_populates="orders")
#     address = relationship("Address")
#     items = relationship("OrderItem", back_populates="order")
#     payment = relationship("Payment", uselist=False, back_populates="order")

# Index("idx_order_status", Order.status)