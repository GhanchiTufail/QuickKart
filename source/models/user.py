from datetime import datetime
from sqlalchemy import Column, Index
from sqlalchemy.orm import relationship
from sqlalchemy import  Integer, String, Float, Boolean, DateTime
from source.config.database import Base, engine

# Core Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # addresses = relationship("Address", back_populates="user")
    # orders = relationship("Order", back_populates="user")
    # wishlist = relationship("Wishlist", back_populates="user")
    # reviews = relationship("Review", back_populates="user")
    # payments = relationship("Payment", back_populates="user")
    # carts = relationship("Cart", back_populates="user")
    # rental_orders = relationship("RentalOrder", back_populates="user")

Base.metadata.create_all(bind=engine)
# Indexes
Index("idx_user_email", User.email)