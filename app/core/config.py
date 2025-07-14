import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    DYNAMODB_REGION: str = os.getenv("DYNAMODB_REGION", "us-east-1")
    DYNAMODB_TABLE: str = os.getenv("DYNAMODB_TABLE", "Licenses")
    DYNAMODB_ENDPOINT_URL: Optional[str] = os.getenv("DYNAMODB_ENDPOINT_URL", None)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings() 