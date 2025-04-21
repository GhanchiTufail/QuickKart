from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Float, Boolean, DateTime, Text, func, LargeBinary, Enum
from source.config.database import Base, engine
from source.utils.categories import CategoryEnum

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    image = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(Enum(CategoryEnum))
    sub_category = Column(String(100), nullable=False)
    stock = Column(Integer, default=0)
    is_rentable = Column(Boolean, default=False)
    daily_rate = Column(Float)
    brand = Column(String(50))
    rating = Column(Float, default=0.0)
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    seller = relationship("Seller", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    rentals = relationship("Rental", back_populates="product")
    notifications = relationship("Notification", back_populates="product")
    #wishlist_items = relationship("Wishlist", back_populates="product")
    #reviews = relationship("Review", back_populates="product")
    # reviews = relationship("Review", back_populates="product")


Base.metadata.create_all(bind=engine)