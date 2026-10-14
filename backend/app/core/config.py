import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Healthcare Hallucination Detection Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB Settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "healthcare_verifier_db")
    
    # ChromaDB & Vector Store Settings
    CHROMADB_DIR: str = os.getenv("CHROMADB_DIR", "./data/chroma_db")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    # NLI & NER Model Settings
    NLI_MODEL_NAME: str = os.getenv("NLI_MODEL_NAME", "cross-encoder/nli-deberta-v3-small")
    BIOBERT_NER_MODEL: str = os.getenv("BIOBERT_NER_MODEL", "dslim/bert-base-NER")
    
    # JWT Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_HEALTHCARE_AI_VERIFICATION_KEY_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 1 day

    class Config:
        case_sensitive = True

settings = Settings()
