from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os
import json


class Settings(BaseSettings):
    """Application settings."""
    
    # Database settings
    database_url: str = Field(
        default="postgresql://medicine_user:medicine_password@postgres:5432/medicine_vending_db",
        env="DATABASE_URL"
    )
    postgres_user: str = Field(default="medicine_user", env="POSTGRES_USER")
    postgres_password: str = Field(default="medicine_password", env="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="medicine_vending_db", env="POSTGRES_DB")
    postgres_host: str = Field(default="postgres", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")
    
    # AI/LLM Configuration
    gemini_api_key: str = Field(default="", env="GEMINI_API_KEY")
    
    # FastAPI Configuration
    secret_key: str = Field(
        default="your-secret-key-change-in-production", 
        env="SECRET_KEY"
    )
    debug: bool = Field(default=True, env="DEBUG")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # CORS Configuration  
    allowed_origins: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000", "http://frontend:5173"],
        env="ALLOWED_ORIGINS"
    )
    
    # External APIs
    pubmed_api_key: Optional[str] = Field(default=None, env="PUBMED_API_KEY")
    wikipedia_api_base_url: str = Field(
        default="https://en.wikipedia.org/api/rest_v1",
        env="WIKIPEDIA_API_BASE_URL"
    )
    
    # App specific settings
    app_name: str = "AI Medicine Vending Machine API"
    version: str = "1.0.0"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse ALLOWED_ORIGINS if it's a JSON string
        if isinstance(self.allowed_origins, str):
            try:
                self.allowed_origins = json.loads(self.allowed_origins)
            except json.JSONDecodeError:
                # If it's not valid JSON, split by comma and strip spaces
                self.allowed_origins = [origin.strip() for origin in self.allowed_origins.split(',')]
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Global settings instance
settings = Settings()
