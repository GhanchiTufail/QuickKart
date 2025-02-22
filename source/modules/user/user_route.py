from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.schemas.user_schema import UserSchema, UserLoginSchema
from source.config.database import get_db
from source.models.user import User
from source.utils.token import create_access_token, get_current_user
router = APIRouter(prefix="/user", tags=["User"])
templates = Jinja2Templates(directory="templates")

# Register Page
@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("user/user_gateway/signup.html", {"request": request})

# Register Backend
@router.post("/register")
async def register_user(
    request: Request,
    user: UserSchema = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return templates.TemplateResponse(
            "user/user_gateway/signup.html",
            {"request": request, "message": "Email already exists"}
        )

    # Create new user
    new_user = User(name=user.name, email=user.email, phone=user.phone, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/user/login", status_code=302)

# Login Page
@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("user/user_gateway/login.html", {"request": request})

# Login Backend
@router.post("/login")
async def login_user(
    request: Request,
    user: UserLoginSchema = Form(...),
    db: Session = Depends(get_db)
):
    user_data = db.query(User).filter(User.email == user.email).first()
    if user_data and user_data.password == user.password:
        access_token = create_access_token(user.email, "user")
        response = RedirectResponse(url="/user/home", status_code=302)
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="lax")
        return response
    else:
        return templates.TemplateResponse(
            "user/user_gateway/login.html",
            {"request": request, "message": "Incorrect email or password"}
        )

# User Dashboard
@router.get("/home")
async def user_dashboard(request: Request, email: dict = Depends(get_current_user)):
    
    return templates.TemplateResponse("user/home.html", {"request": request, "email":email["name"]})

















# from fastapi import APIRouter, Request, Depends, Form
# from fastapi.templating import Jinja2Templates
# from source.schemas.user_schema import UserSchema, UserLoginSchema
# from sqlalchemy.orm import Session
# from source.config.database import get_db
# from source.models.user import User
# from fastapi.responses import RedirectResponse

# router = APIRouter(prefix="/user", tags=["User"])
# templates = Jinja2Templates(directory="templates")

# @router.get("/register")
# async def register_page(request: Request):
#     return templates.TemplateResponse("user/user_gateway/signup.html", {"request": request})

# @router.post("/register")
# async def create_user(
#     request: Request,
#     user: UserSchema = Form(...),
#     db: Session = Depends(get_db)
# ):
#     query = db.query(User).filter(User.email == user.email)
#     if query:
#         return templates.TemplateResponse(
#             "user/user_gateway/signup.html",
#             {"request":request, "message":"email already exist"})
#     # Create new user
#     new_user = User(name=user.name,email=user.email,phone=user.phone,password=user.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     return RedirectResponse(url="/user/home", status_code=303)

# # login frontend
# @router.get("/login")
# async def login_page(request: Request):
#     return templates.TemplateResponse("user/user_gateway/login.html", {"request": request})

# # login backend
# @router.post("/login")
# async def create_user(
#     request: Request,
#     user: UserLoginSchema = Form(...),
#     db: Session = Depends(get_db)
# ):
#     admin_data = db.query(User).filter(User.email == user.email).first()
#     if admin_data and admin_data.password == user.password:
#         return templates.TemplateResponse(
#             "/user/home.html", {"request": request, "message": "Login successful!"}
#         )
#     else:
#         return templates.TemplateResponse(
#             "user/user_gateway/login.html", {"request": request, "message": "Incorrect email or password"}
#         )
    

# #admin dashboard
# @router.get("/home")
# async def admin_dashboard(request: Request):
#     return templates.TemplateResponse("user/home.html", {"request": request})