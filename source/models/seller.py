from sqlalchemy import Column, func, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from source.config.database import Base,engine

class Seller(Base):
    __tablename__ = "sellers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    store_name = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True, nullable=False)  # New field for contact number
    is_verified = Column(Boolean, default=False)  # New field for seller verification
    rating = Column(Float, nullable=True)  # Optional field for seller rating
    balance = Column(Float, default=0.0)  # Earnings/balance

    created_at = Column(DateTime, default=func.now())  # Auto-generate timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Auto-update timestamp

    #products = relationship("Product", back_populates="seller")  # Relationship with Product model

Base.metadata.create_all(bind=engine)