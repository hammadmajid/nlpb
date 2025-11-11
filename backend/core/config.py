"""
Core configuration for NLPB application.
"""
from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings."""
    
    # API Settings
    API_TITLE: str = "NLP Business Intelligence API"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "API for sentiment analysis, resume screening, and fake news detection"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # CORS Settings
    CORS_ORIGINS: list[str] = ["http://localhost:8501", "http://localhost:3000"]
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "./data/uploads"
    
    # Model Settings
    MIN_CONFIDENCE_THRESHOLD: float = 0.5


settings = Settings()
