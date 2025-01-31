import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_jwt_secret")