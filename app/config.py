import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from limits.storage import RedisStorage

# Load environment variables from .env file
load_dotenv()

# ✅ Move `Limiter` outside the class
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    strategy="moving-window"
)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_jwt_secret")
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")  # Allow all origins by default
    