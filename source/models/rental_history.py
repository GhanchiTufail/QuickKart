# from datetime import datetime
# from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, Float, Boolean, func
# from sqlalchemy.orm import relationship
# from source.config.database import Base, engine


# class RentalHistory(Base):
#     __tablename__ = "rental_history"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
#     start_date = Column(DateTime, nullable=False)
#     end_date = Column(DateTime, nullable=False)
#     total_price = Column(Float, nullable=False)
#     status = Column(String(20), nullable=False)  # completed, canceled, refunded
#     is_history = Column(Boolean, default=False)
#     created_at = Column(DateTime, default=func.now())

#     # Relationships
#     user = relationship("User")
#     product = relationship("Product")