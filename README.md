# 🛒 QuickKart

QuickKart is a feature-rich **E-commerce platform** developed using **FastAPI** (Python) for the backend and **HTML, CSS, JavaScript** for the frontend. It supports three roles—**Admin**, **Seller**, and **Customer**—each with role-specific functionalities. The system is designed for performance, scalability, and security, with cloud-based image handling and PostgreSQL database integration.

---

## 📌 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [User Roles & Features](#-user-roles--features)
- [Image Handling](#-image-handling)
- [Authentication & Security](#-authentication--security)
- [Database Migrations](#-database-migrations)
- [Running the Project](#-running-the-project)
- [Testing the API](#-testing-the-api)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🔧 Tech Stack

### ✅ Backend
- **FastAPI** – High-performance Python web framework
- **SQLAlchemy** – ORM for database interactions
- **Alembic** – Database migration tool
- **PostgreSQL** – Relational database
- **psycopg2** – PostgreSQL adapter for Python
- **Passlib[bcrypt]** – Secure password hashing
- **Cloudinary** – Image uploading and CDN
- **python-multipart** – For handling file uploads
- **Jinja2** – Templating engine
- **Uvicorn** – ASGI server for running FastAPI

### 🎨 Frontend
- **HTML**
- **CSS**
- **JavaScript**

---


---

## 👥 User Roles & Features

### 👑 Admin
- View all customers, sellers, and products
- View individual seller’s uploaded products
- Ban sellers for violating policies

### 🧑‍💼 Seller
- Upload, edit, and delete products
- View notifications when a product is purchased

### 🛍 Customer
- Browse products and view details
- Add products to cart
- Make purchases
- Receive notifications after a purchase

---

## 🖼 Image Handling

- Product images are uploaded using **Cloudinary**, allowing for:
  - Secure cloud storage
  - Faster image delivery
  - Optimized performance

---

## 🔐 Authentication & Security

- **JWT-based authentication** for secure session management
- **Passlib (bcrypt)** for strong password encryption
- Role-based access control ensures each user only accesses their allowed features

---

## 🔄 Database Migrations

Use **Alembic** for schema version control and applying changes safely:


alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 🚀 QuickKart

---

## 🚀 Running the Project

### 1. Clone the Repository

git clone https://github.com/yourusername/QuickKart.git
cd QuickKart

### 2. Create Virtual Environment

python -m venv env
source env/bin/activate # On Windows: env\Scripts\activate


### 3. Install Dependencies

pip install -r requirements.txt


### 4. Configure Environment Variables

Create a `.env` file in the root directory:

env
DATABASE_URL=postgresql://username:password@localhost/quickkart
SECRET_KEY=your_secret_key
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name



### 5. Run the Server

uvicorn source.main:app --reload



---

## 🧪 Testing the API

Access Swagger UI at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

Access ReDoc at:  
[http://localhost:8000/redoc](http://localhost:8000/redoc)

Both are auto-generated and interactive API docs powered by FastAPI.

---

## 🚧 Future Enhancements

- 🧾 Integration with a payment gateway (Stripe, Razorpay)  
- ⭐ Product reviews and rating system  
- 🛒 Wishlist functionality  
- 📦 Order history and tracking for customers  
- 📊 Admin dashboard with insights and analytics  

---

## 🤝 Contributing

Fork the repository

Create your feature branch:  
git checkout -b feature/YourFeatureName



Commit your changes:  
git commit -m 'Add YourFeatureName'



Push to the branch:  
git push origin feature/YourFeatureName



Open a pull request

---

## 📝 License

This project is licensed under the MIT License – see the LICENSE file for details.

---

## 🙌 Acknowledgements

- FastAPI Documentation  
- Cloudinary  
- SQLAlchemy  
- Alembic  
- PostgreSQL
