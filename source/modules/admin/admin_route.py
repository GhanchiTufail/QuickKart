from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from source.schemas.admin_schema import AdminSchema
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.admin import Admin

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("admin_gateway/signup.html", {"request": request})

@router.post("/register")
async def create_user(
    request: Request,
    admin: AdminSchema = Form(...),
    db: Session = Depends(get_db)
):
    # Create new user
    new_user = Admin(email=admin.email,password=admin.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request, "message": "User created successfully!"}
    )


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("admin_gateway/login.html", {"request": request})

@router.post("/register")
async def create_user(
    request: Request,
    admin: AdminSchema = Form(...),
    db: Session = Depends(get_db)
):
    admin_data = db.query(Admin).filter(Admin.email == admin.email).first()
    if admin_data and admin_data.password == admin.password:
        return templates.TemplateResponse(
            "admin_dashboard.html", {"request": request, "message": "Login successful!"}
        )
    else:
        return templates.TemplateResponse(
            "admin_gateway/login.html", {"request": request, "message": "Incorrect email or password"}
        )