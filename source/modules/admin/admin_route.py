from fastapi import APIRouter, Request, Depends, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.admin import Admin
from source.utils.hashing import verify_password, hash_password
from source.utils.token import create_access_token, get_current_admin
from source.schemas.admin_schema import AdminSchema

router = APIRouter(prefix="/admin", tags=["Admin"])
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
    query = db.query(Admin).filter(Admin.email == admin.email).first()
    if query:
        return templates.TemplateResponse(
            "admin_gateway/signup.html",
            {"request": request, "message": "Email already exists"},
        )
    # Create new admin
    new_admin = Admin(email=admin.email, password=hash_password(admin.password))
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    return RedirectResponse(url="/admin/login", status_code=303)

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("admin_gateway/login.html", {"request": request})

@router.post("/login")
async def login_admin(
    request: Request,
    admin: AdminSchema = Form(...),
    db: Session = Depends(get_db),
):
    admin_data = db.query(Admin).filter(Admin.email == admin.email).first()
    if admin_data and verify_password(admin.password, admin_data.password):
        # Create JWT token
        access_token = create_access_token(admin.email, "admin")
        # Set token in cookies
        #return {"token":access_token}
        response = RedirectResponse(url="/admin/admin_dashboard", status_code=303)
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="lax")
        return response
    else:
        return templates.TemplateResponse(
            "admin_gateway/login.html",
            {"request": request, "message": "Incorrect email or password"},
        )

# Admin dashboard (protected)
@router.get("/admin_dashboard")
async def admin_dashboard(
    request: Request,
    email: str = Depends(get_current_admin)
):
    # return {"Email":email}
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request, "email": email},
    )