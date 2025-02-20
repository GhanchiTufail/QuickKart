from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE = "postgresql://postgres:1234@localhost:5432/QuickKart"
engine = create_engine(DATABASE)
Base = declarative_base()
sessionlocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)
def get_db():
    db = sessionlocal()
    try:
        yield db
    except:
        db.close()