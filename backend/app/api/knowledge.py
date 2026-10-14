from fastapi import APIRouter
from typing import List
from app.models.schemas import KnowledgeSourceItem

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])

@router.get("/sources", response_model=List[KnowledgeSourceItem])
async def list_knowledge_sources():
    """
    Returns active indexed healthcare guidelines in the RAG vector store.
    """
    return [
        KnowledgeSourceItem(
            id="kb_who_001",
            title="WHO Therapeutics and COVID-19 Living Guideline",
            source_organization="World Health Organization (WHO)",
            domain="Infectious Diseases / Therapeutics",
            doc_type="Clinical Practice Guideline",
            publication_year=2023,
            chunks_count=450
        ),
        KnowledgeSourceItem(
            id="kb_fda_002",
            title="FDA Drug Safety & Ivermectin Warning Communication",
            source_organization="U.S. Food and Drug Administration (FDA)",
            domain="Pharmacology / Regulatory Safety",
            doc_type="Regulatory Safety Advisory",
            publication_year=2023,
            chunks_count=120
        ),
        KnowledgeSourceItem(
            id="kb_nih_003",
            title="NIH COVID-19 Treatment Guidelines Panel Report",
            source_organization="National Institutes of Health (NIH)",
            domain="Clinical Therapeutics",
            doc_type="Clinical Guideline",
            publication_year=2024,
            chunks_count=680
        ),
        KnowledgeSourceItem(
            id="kb_ada_004",
            title="ADA Standards of Care in Diabetes 2024",
            source_organization="American Diabetes Association (ADA)",
            domain="Endocrinology / Metabolism",
            doc_type="Clinical Benchmark",
            publication_year=2024,
            chunks_count=890
        ),
        KnowledgeSourceItem(
            id="kb_cdc_005",
            title="CDC Adult Outpatient Pneumonia Antibiotic Stewardship",
            source_organization="Centers for Disease Control and Prevention (CDC)",
            domain="Infectious Diseases / Pharmacology",
            doc_type="Clinical Practice Standard",
            publication_year=2023,
            chunks_count=340
        )
    ]
