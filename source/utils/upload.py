import os
import cloudinary
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

Configure  = cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)