from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class MongoUser(BaseModel):
    id: Optional[str] = Field(alias="_id")
    email: str
    username: str
    hashed_password: str
    role: str = "researcher"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MongoVerificationReport(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: Optional[str] = None
    query: str
    llm_response: str
    llm_model: str
    overall_confidence_score: float
    hallucination_detected: bool
    total_claims: int
    hallucinated_claims: int
    claims_detail: List[Dict[str, Any]]
    summary_report: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MongoKnowledgeDocument(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str
    source_org: str  # WHO, CDC, NIH, PubMed, FDA
    domain: str       # Cardiology, Oncology, Pharmacology, Pediatrics, Infectious Diseases
    url: Optional[str] = None
    content: str
    chunk_count: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
