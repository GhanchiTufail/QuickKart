from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
# from source.config.database import engine
from source.config.database import get_db
from source.schemas.admin_schema import AdminSchema
from source.models.admin import Admin
from source.modules.admin import admin_route
from source.modules.user import user_route
from source.modules.seller import seller_route

app = FastAPI()

app.include_router(admin_route.router)
app.include_router(user_route.router)
app.include_router(seller_route.router)

# # Create database tables
# # User.metadata.create_all(bind=engine)

# app = FastAPI()

# # Configure templates for Jinja2
# templates = Jinja2Templates(directory="templates")



# @app.get("/submit")
# async def login_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @app.post("/submit")
# async def create_user(
#     request: Request,
#     admin: AdminSchema = Form(...),
#     db: Session = Depends(get_db)
# ):
#     # Create new user
#     new_user = Admin(email=admin.email,password=admin.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     return templates.TemplateResponse(
#         "/abc/def/home.html",
#         {"request": request, "message": "User created successfully!"}
#     )


# # @app.get("/submit")
# # async def login_page(request: Request):
# #     return templates.TemplateResponse("login.html", {"request": request})

# # @app.post("/submit")
# # async def create_user(
# #     request: Request,
# #     name: str = Form(...),
# #     db: Session = Depends(get_db)
# # ):
# #     # Create new user
# #     new_user = User(name=name)
# #     db.add(new_user)
# #     db.commit()
# #     db.refresh(new_user)
    
# #     return templates.TemplateResponse(
# #         "login.html",
# #         {"request": request, "message": "User created successfully!"}
# #     )

# # # New route to display all users
# # @app.get("/users")
# # async def list_users(request: Request, db: Session = Depends(get_db)):
# #     # Fetch all users from the database
# #     users = db.query(User).all()
# #     return templates.TemplateResponse(
# #         "abc/def/home.html",  # Path to the home.html file
# #         {"request": request, "users": users}
# #     )