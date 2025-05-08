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

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
