import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_jwt_secret")
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")  # Allow all origins by default

    # Rate Limit Settings
    RATE_LIMIT = os.getenv("RATE_LIMIT", "8 per minute")  # Default: 8 requests per minute
    