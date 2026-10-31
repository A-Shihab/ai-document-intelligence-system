import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DocIntel AI"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    GEMINI_API_KEY: str
    DATABASE_URL: str
    UPLOAD_DIR: str = "./data/uploads"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure upload directory exists locally
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)