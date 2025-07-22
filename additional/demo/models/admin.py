from sqlalchemy import Column, func
from sqlalchemy import Integer, String, DateTime
from ..config.database import Base, engine

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

Base.metadata.create_all(bind=engine)