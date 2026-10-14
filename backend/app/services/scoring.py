from typing import List, Dict, Any

class ConfidenceScoringAlgorithm:
    """
    Multi-Factorial Confidence Scoring Algorithm:
    Calculates a quantitative trustworthiness score (0.0 to 1.0 or 0-100%) for medical claims and full LLM responses.
    
    Formula:
    Confidence = w1 * Similarity_Score + w2 * Entailment_Score + w3 * Source_Authority_Weight - w4 * Contradiction_Penalty
    """
    def __init__(self):
        self.w_sim = 0.30        # Weight for Vector Similarity
        self.w_entail = 0.40     # Weight for NLI Entailment
        self.w_authority = 0.30  # Weight for Guideline Authority (WHO/CDC/FDA = 1.0)
        self.w_contradict = 0.50 # Penalty multiplier for NLI Contradiction

    def calculate_claim_confidence(
        self,
        verdict: str,
        similarity_score: float,
        entailment_score: float,
        contradiction_score: float,
        evidences: List[Dict[str, Any]]
    ) -> float:
        # Determine average source authority weight (WHO/CDC/FDA = 1.0, PubMed = 0.85, General = 0.7)
        authority_weights = []
        for ev in evidences:
            source = ev.get("source_name", "").lower()
            if any(s in source for s in ["who", "cdc", "fda", "nih"]):
                authority_weights.append(1.0)
            elif "pubmed" in source or "journal" in source:
                authority_weights.append(0.85)
            else:
                authority_weights.append(0.70)
        
        avg_authority = float(sum(authority_weights) / len(authority_weights)) if authority_weights else 0.5

        if verdict == "REFUTES":
            # If refutes (hallucinated), confidence in claim validity drops, but confidence in hallucination detection is high.
            # Here we return confidence in the claim's factual accuracy (which will be low for hallucinated claims).
            base_score = (self.w_sim * similarity_score) + (self.w_authority * avg_authority)
            score = max(0.05, base_score - (self.w_contradict * contradiction_score))
        elif verdict == "SUPPORTS":
            score = (self.w_sim * similarity_score) + (self.w_entail * entailment_score) + (self.w_authority * avg_authority)
            score = min(0.99, score)
        else: # NOT_ENOUGH_INFO
            score = 0.35 + (0.15 * similarity_score)

        return round(float(score), 4)

    def calculate_overall_confidence(self, claim_results: List[Dict[str, Any]]) -> float:
        if not claim_results:
            return 0.50

        scores = [c.get("confidence_score", 0.5) for c in claim_results]
        verdicts = [c.get("verdict") for c in claim_results]

        # Heavy penalty if any critical treatment claim is hallucinated/refuted
        has_hallucination = any(v == "REFUTES" for v in verdicts)
        avg_score = float(sum(scores) / len(scores))

        if has_hallucination:
            overall = max(0.10, avg_score * 0.60)
        else:
            overall = avg_score

        return round(float(overall), 4)

scoring_engine = ConfidenceScoringAlgorithm()
