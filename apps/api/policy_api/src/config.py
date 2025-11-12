"""
Configuration settings for Policy API
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://policy_user:policy_pass@policy_db:5432/policy_db"
    
    # OPAL Configuration
    OPAL_SERVER_URL: str = "http://opal_publisher:7002"
    OPAL_AUTH_TOKEN: str = "super-secret-token"
    OPAL_POLICY_TOPIC: str = "policy_data"
    
    # Keycloak Configuration
    KEYCLOAK_URL: str = "http://keycloak:8080"
    KEYCLOAK_REALM: str = "my-app"
    KEYCLOAK_CLIENT_ID: str = "policy-api"
    KEYCLOAK_CLIENT_SECRET: Optional[str] = None
    
    # Application Settings
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    API_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()