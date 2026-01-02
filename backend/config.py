import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # Groq LLM Settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_PRIMARY_MODEL: str = os.getenv("GROQ_PRIMARY_MODEL", "llama-3.3-70b-versatile")
    GROQ_FAST_MODEL: str = os.getenv("GROQ_FAST_MODEL", "llama-3.1-8b-instant")
    GROQ_CLASSIFIER_MODEL: str = os.getenv("GROQ_CLASSIFIER_MODEL", "gemma-2-9b-it")
    GROQ_MAX_TOKENS: int = int(os.getenv("GROQ_MAX_TOKENS", "4096"))
    GROQ_TIMEOUT: int = int(os.getenv("GROQ_TIMEOUT", "60"))
    
    # Weather Service Settings
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    DEFAULT_CITY: str = os.getenv("DEFAULT_CITY", "New York")
    DEFAULT_LOCATION: str = os.getenv("DEFAULT_LOCATION", "North America")
    ENABLE_REAL_TIME_WEATHER: bool = os.getenv("ENABLE_REAL_TIME_WEATHER", "True").lower() == "true"
    
    # Market Service Settings
    USDA_API_KEY: str = os.getenv("USDA_API_KEY", "")
    AGMARKNET_API_KEY: str = os.getenv("AGMARKNET_API_KEY", "")
    ENABLE_REAL_TIME_MARKET: bool = os.getenv("ENABLE_REAL_TIME_MARKET", "False").lower() == "true"
    
    # Cache Settings
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "False").lower() == "true"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Feature Flags
    ENABLE_LLM_FALLBACK: bool = os.getenv("ENABLE_LLM_FALLBACK", "True").lower() == "true"

    # Supabase / Database Settings
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    # Try multiple possible key names for flexibility
    SUPABASE_KEY: str = (
        os.getenv("SUPABASE_KEY") or 
        os.getenv("SUPABASE_ANON_KEY") or 
        os.getenv("SUPABASE_SERVICE_ROLE_KEY") or 
        ""
    )
    ENABLE_REAL_DB: bool = os.getenv("ENABLE_REAL_DB", "False").lower() == "true"

    class Config:
        case_sensitive = True

settings = Settings()
