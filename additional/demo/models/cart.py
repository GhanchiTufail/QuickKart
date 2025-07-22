from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import relationship
from source.config.database import Base, engine  # Assuming you have a database.py for SQLAlchemy setup
from source.models.product import Product  # Importing the Product model

class Cart(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    amount = Column(Numeric(18, 2), nullable=False)
    added_at = Column(DateTime, default=func.now())

    # Relationship with Product model
    product = relationship("Product")

Base.metadata.create_all(bind=engine)