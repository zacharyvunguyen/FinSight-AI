from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FinSight AI"
    
    # Security
    DEBUG_MODE: bool = False
    
    # Storage Paths
    PDF_STORAGE_PATH: str
    PROCESSED_DATA_PATH: str
    
    # Google Cloud
    GOOGLE_CLOUD_PROJECT: str
    GCP_STORAGE_BUCKET: str
    BIGQUERY_DATASET: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    
    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_CLOUD: str
    PINECONE_REGION: str
    PINECONE_INDEX_NAME: str
    PINECONE_ENVIRONMENT: str
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # Llama Cloud
    LLAMA_CLOUD_API_KEY: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 