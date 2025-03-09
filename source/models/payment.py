from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from source.config.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    status = Column(String, default="Pending")  # Pending, Completed
    payment_method = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    order = relationship("Order")
    user = relationship("User")
