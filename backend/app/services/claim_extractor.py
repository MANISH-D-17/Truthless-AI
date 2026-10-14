import re
from typing import List, Dict, Any
import uuid

class MedicalClaimExtractor:
    """
    NLP Claim Extraction Engine:
    Decomposes LLM medical responses into discrete, testable atomic claim statements.
    Filters out conversational fluff, introductory greetings, and disclaimer filler.
    """
    def __init__(self):
        self.disclaimer_patterns = [
            r"as an ai", r"consult your doctor", r"i am not a doctor",
            r"always seek medical advice", r"in summary", r"here is what i found"
        ]

    def extract_claims(self, text: str) -> List[Dict[str, Any]]:
        # Clean text and split into candidate sentences
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        claims = []

        for sent in sentences:
            sent_clean = sent.strip()
            if len(sent_clean) < 15:
                continue
            
            # Filter non-factual greetings & standard AI disclaimers
            if any(re.search(pat, sent_clean, re.IGNORECASE) for pat in self.disclaimer_patterns):
                continue
                
            # Clause splitting for complex sentences with sub-claims
            sub_clauses = re.split(r';|\b(furthermore|moreover|additionally|however)\b', sent_clean, flags=re.IGNORECASE)
            for clause in sub_clauses:
                if not clause or len(clause.strip()) < 15:
                    continue
                c_clean = clause.strip()
                # Ensure statement contains medical/actionable assertions
                if self._is_factual_assertion(c_clean):
                    claims.append({
                        "claim_id": f"claim_{uuid.uuid4().hex[:8]}",
                        "claim_text": c_clean,
                        "category": self._categorize_claim(c_clean)
                    })

        # If no distinct claims extracted, return the whole text as a single claim
        if not claims and text.strip():
            claims.append({
                "claim_id": f"claim_{uuid.uuid4().hex[:8]}",
                "claim_text": text.strip(),
                "category": "General Medical Assertion"
            })

        return claims

    def _is_factual_assertion(self, sentence: str) -> bool:
        # Rules to verify sentence asserts medical facts (drug, dosage, treatment, diagnosis, etiology)
        medical_keywords = [
            "treat", "prescribe", "dosage", "mg", "side effect", "cause", "symptom",
            "inhibitor", "approved", "fda", "vaccine", "indicated", "diagnosis",
            "contraindicated", "mortality", "efficacy", "clinical trial", "cure", "virus",
            "bacterial", "infection", "cancer", "therapy", "recommended"
        ]
        sent_lower = sentence.lower()
        return any(kw in sent_lower for kw in medical_keywords) or len(sentence.split()) >= 6

    def _categorize_claim(self, claim_text: str) -> str:
        text_lower = claim_text.lower()
        if any(w in text_lower for w in ["mg", "dose", "daily", "oral", "intravenous"]):
            return "Pharmacology & Dosage"
        elif any(w in text_lower for w in ["treat", "therapy", "prescribed", "cure", "first-line"]):
            return "Treatment & Therapeutics"
        elif any(w in text_lower for w in ["side effect", "risk", "toxicity", "adverse", "contraindicated"]):
            return "Safety & Contraindications"
        elif any(w in text_lower for w in ["symptom", "cause", "diagnosed", "sign", "marker"]):
            return "Diagnosis & Pathology"
        return "General Medical Assertion"

claim_extractor = MedicalClaimExtractor()
