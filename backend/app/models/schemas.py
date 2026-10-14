from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Authentication Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: Optional[str] = "researcher"

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# --- Verification & Claim Schemas ---
class ClaimVerificationRequest(BaseModel):
    query: str
    llm_response: str
    llm_model: Optional[str] = "Llama-3-8B-Instruct"

class SingleClaimRequest(BaseModel):
    claim_text: str

class MedicalEntity(BaseModel):
    text: str
    label: str
    start: int
    end: int

class ClaimExtractionResult(BaseModel):
    claim_id: str
    claim_text: str
    entities: List[MedicalEntity]
    category: Optional[str] = "General Medical Claim"

class EvidenceItem(BaseModel):
    source_name: str
    title: str
    url: Optional[str] = None
    excerpt: str
    similarity_score: float
    evidence_level: Optional[str] = "High (WHO/CDC/PubMed)"

class SingleClaimVerificationResult(BaseModel):
    claim_id: str
    claim_text: str
    entities: List[MedicalEntity]
    verdict: str  # SUPPORTS, REFUTES, NOT_ENOUGH_INFO
    confidence_score: float
    entailment_score: float
    contradiction_score: float
    neutral_score: float
    evidences: List[EvidenceItem]
    explanation: str

class FullVerificationResponse(BaseModel):
    session_id: str
    query: str
    original_llm_response: str
    overall_confidence_score: float
    hallucination_detected: bool
    hallucinated_claims_count: int
    total_claims_count: int
    claims_verification: List[SingleClaimVerificationResult]
    summary_report: str
    timestamp: datetime

# --- Knowledge Base Schemas ---
class KnowledgeSourceItem(BaseModel):
    id: str
    title: str
    source_organization: str
    domain: str
    doc_type: str
    publication_year: int
    chunks_count: int
