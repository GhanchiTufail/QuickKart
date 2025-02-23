from fastapi import Request, Depends, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.admin import Admin
from source.utils.hashing import verify_password, hash_password
from source.utils.token import create_access_token, get_current_admin
from source.schemas.admin_schema import AdminSchema

templates = Jinja2Templates(directory="templates")


def create_admin_service(request: Request, admin: AdminSchema, db: Session):
    try:
        query = db.query(Admin).filter(Admin.email == admin.email).first()
        if query:
            return False
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error in checking if admin exist or not")
    try:
        new_admin = Admin(email=admin.email, password=hash_password(admin.password))
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return True
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating admin")


def login_admin_service(admin: AdminSchema = Form(...), db: Session = Depends(get_db)):
    try:
        admin_data = db.query(Admin).filter(Admin.email == admin.email).first()
        if admin_data and verify_password(admin.password, admin_data.password):
            access_token = create_access_token(admin.email, "admin")
            return access_token
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error while creating admin token")