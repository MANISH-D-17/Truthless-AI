from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
import uuid

from app.models.schemas import (
    ClaimVerificationRequest, SingleClaimRequest,
    FullVerificationResponse, SingleClaimVerificationResult,
    EvidenceItem, MedicalEntity
)
from app.services.claim_extractor import claim_extractor
from app.services.medical_ner import medical_ner
from app.services.vector_store import vector_store
from app.services.verifier import verifier
from app.services.scoring import scoring_engine
from app.services.explainability import explainability_engine
from app.core.database import get_database

router = APIRouter(prefix="/verify", tags=["Verification Engine"])

@router.post("", response_model=FullVerificationResponse)
async def verify_llm_response(payload: ClaimVerificationRequest):
    """
    Main Verification Gateway:
    1. Extracts atomic medical claims from LLM response.
    2. Identifies medical entities using BioBERT NER.
    3. Retrieves top-k evidence passages via ChromaDB RAG.
    4. Evaluates claim factual stance using NLI.
    5. Calculates confidence scores & generates explainability audit report.
    """
    query = payload.query
    llm_response = payload.llm_response
    
    if not llm_response.strip():
        raise HTTPException(status_code=400, detail="LLM response body cannot be empty.")

    # Step 1: Claim Extraction
    raw_claims = claim_extractor.extract_claims(llm_response)
    
    claims_verification_list: List[SingleClaimVerificationResult] = []
    hallucinated_count = 0

    for item in raw_claims:
        claim_id = item["claim_id"]
        claim_text = item["claim_text"]
        category = item["category"]

        # Step 2: BioBERT NER
        ner_entities = medical_ner.extract_entities(claim_text)
        entities_schema = [
            MedicalEntity(
                text=ent["text"],
                label=ent["label"],
                start=ent["start"],
                end=ent["end"]
            ) for ent in ner_entities
        ]

        # Step 3: RAG Retrieval from ChromaDB
        evidence_dicts = vector_store.search_evidence(claim_text, top_k=3)
        evidences_schema = [
            EvidenceItem(
                source_name=ev["source_name"],
                title=ev["title"],
                url=ev.get("url"),
                excerpt=ev["excerpt"],
                similarity_score=ev["similarity_score"],
                evidence_level=ev.get("evidence_level")
            ) for ev in evidence_dicts
        ]

        # Step 4: Fact Verification (NLI)
        nli_res = verifier.verify_claim_against_evidences(claim_text, evidence_dicts)
        verdict = nli_res["verdict"]

        if verdict == "REFUTES":
            hallucinated_count += 1

        # Step 5: Confidence Scoring
        top_sim = max([e.similarity_score for e in evidences_schema], default=0.5)
        claim_confidence = scoring_engine.calculate_claim_confidence(
            verdict=verdict,
            similarity_score=top_sim,
            entailment_score=nli_res["entailment_score"],
            contradiction_score=nli_res["contradiction_score"],
            evidences=evidence_dicts
        )

        # Step 6: Claim Explanation
        explanation = explainability_engine.generate_claim_explanation(
            claim_text=claim_text,
            verdict=verdict,
            confidence_score=claim_confidence,
            evidences=evidence_dicts
        )

        claims_verification_list.append(
            SingleClaimVerificationResult(
                claim_id=claim_id,
                claim_text=claim_text,
                entities=entities_schema,
                verdict=verdict,
                confidence_score=claim_confidence,
                entailment_score=nli_res["entailment_score"],
                contradiction_score=nli_res["contradiction_score"],
                neutral_score=nli_res["neutral_score"],
                evidences=evidences_schema,
                explanation=explanation
            )
        )

    # Step 7: Aggregate Response Scoring & XAI Summary Report
    claim_dicts_for_scoring = [c.dict() for c in claims_verification_list]
    overall_confidence = scoring_engine.calculate_overall_confidence(claim_dicts_for_scoring)
    
    summary_report = explainability_engine.generate_summary_report(
        query=query,
        total_claims=len(claims_verification_list),
        hallucinated_claims=hallucinated_count,
        overall_confidence=overall_confidence,
        claim_details=claim_dicts_for_scoring
    )

    session_id = f"sess_{uuid.uuid4().hex[:10]}"
    timestamp = datetime.utcnow()

    response_payload = FullVerificationResponse(
        session_id=session_id,
        query=query,
        original_llm_response=llm_response,
        overall_confidence_score=overall_confidence,
        hallucination_detected=(hallucinated_count > 0),
        hallucinated_claims_count=hallucinated_count,
        total_claims_count=len(claims_verification_list),
        claims_verification=claims_verification_list,
        summary_report=summary_report,
        timestamp=timestamp
    )

    # Step 8: Persist to MongoDB Audit Log
    db_conn = await get_database()
    if db_conn is not None:
        try:
            await db_conn["verification_reports"].insert_one(response_payload.dict())
        except Exception as e:
            print(f"MongoDB persistence notice: {e}")

    return response_payload

@router.post("/single-claim", response_model=SingleClaimVerificationResult)
async def verify_single_claim(payload: SingleClaimRequest):
    claim_text = payload.claim_text.strip()
    if not claim_text:
        raise HTTPException(status_code=400, detail="Claim text required.")

    ner_entities = medical_ner.extract_entities(claim_text)
    entities_schema = [MedicalEntity(text=e["text"], label=e["label"], start=e["start"], end=e["end"]) for e in ner_entities]
    
    evidence_dicts = vector_store.search_evidence(claim_text, top_k=3)
    evidences_schema = [EvidenceItem(**ev) for ev in evidence_dicts]
    
    nli_res = verifier.verify_claim_against_evidences(claim_text, evidence_dicts)
    verdict = nli_res["verdict"]

    top_sim = max([e.similarity_score for e in evidences_schema], default=0.5)
    conf = scoring_engine.calculate_claim_confidence(
        verdict=verdict,
        similarity_score=top_sim,
        entailment_score=nli_res["entailment_score"],
        contradiction_score=nli_res["contradiction_score"],
        evidences=evidence_dicts
    )

    explanation = explainability_engine.generate_claim_explanation(
        claim_text=claim_text,
        verdict=verdict,
        confidence_score=conf,
        evidences=evidence_dicts
    )

    return SingleClaimVerificationResult(
        claim_id=f"claim_{uuid.uuid4().hex[:8]}",
        claim_text=claim_text,
        entities=entities_schema,
        verdict=verdict,
        confidence_score=conf,
        entailment_score=nli_res["entailment_score"],
        contradiction_score=nli_res["contradiction_score"],
        neutral_score=nli_res["neutral_score"],
        evidences=evidences_schema,
        explanation=explanation
    )
