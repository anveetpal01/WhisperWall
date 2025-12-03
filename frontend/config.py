import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
    APP_TITLE = os.getenv("APP_TITLE", "Anonymous Blog")
    MAX_POST_LENGTH = int(os.getenv("MAX_POST_LENGTH", "5000"))
    POSTS_PER_PAGE = int(os.getenv("POSTS_PER_PAGE", "20"))


config = Config()