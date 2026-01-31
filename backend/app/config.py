from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./blog.db"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Anonymous Blog"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Posts
    MAX_POST_LENGTH: int = 5000
    POSTS_PER_PAGE: int = 20
    
    # Security
    SECRET_KEY: str = "06A01BAF68A81BCF8830EB232C7760C1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
