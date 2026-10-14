from typing import List, Dict, Any

class ExplainableAIEngine:
    """
    Explainable AI (XAI) & Audit Report Generator:
    Provides transparent, clinically interpretable explanations for verified claims and hallucinations.
    Identifies contradictory evidence passages, highlights unverified tokens, and computes clinical risk levels.
    """
    def generate_claim_explanation(
        self,
        claim_text: str,
        verdict: str,
        confidence_score: float,
        evidences: List[Dict[str, Any]]
    ) -> str:
        conf_pct = round(confidence_score * 100, 1)
        
        if verdict == "REFUTES":
            explanation = (
                f"⚠️ **HALLUCINATION / CONTRADICTION DETECTED** (Confidence: {conf_pct}%)\n"
                f"The claim '{claim_text}' directly contradicts official healthcare guidelines. "
            )
            if evidences:
                top_ev = evidences[0]
                explanation += (
                    f"Refuting Evidence from **{top_ev.get('source_name')}** ({top_ev.get('title')}): "
                    f"\"{top_ev.get('excerpt')}\""
                )
            return explanation
            
        elif verdict == "SUPPORTS":
            explanation = (
                f"✅ **VERIFIED CLAIM** (Confidence: {conf_pct}%)\n"
                f"The claim '{claim_text}' is factually corroborated by trusted clinical sources. "
            )
            if evidences:
                top_ev = evidences[0]
                explanation += (
                    f"Supporting evidence from **{top_ev.get('source_name')}**: "
                    f"\"{top_ev.get('excerpt')}\""
                )
            return explanation

        else: # NOT_ENOUGH_INFO
            return (
                f"❓ **UNVERIFIABLE / INSUFFICIENT EVIDENCE** (Confidence: {conf_pct}%)\n"
                f"The claim '{claim_text}' could not be definitively matched or validated against current WHO/CDC/PubMed indices. "
                "Manual clinical verification is required."
            )

    def generate_summary_report(
        self,
        query: str,
        total_claims: int,
        hallucinated_claims: int,
        overall_confidence: float,
        claim_details: List[Dict[str, Any]]
    ) -> str:
        risk_level = "CRITICAL HIGH" if hallucinated_claims > 0 else ("MODERATE" if overall_confidence < 0.75 else "LOW / VERIFIED")
        
        report = [
            f"# Clinical Verification Audit Report",
            f"**Query**: {query}",
            f"**Overall Factual Confidence Score**: {round(overall_confidence * 100, 1)}%",
            f"**Clinical Risk Level**: {risk_level}",
            f"**Total Claims Evaluated**: {total_claims}",
            f"**Hallucinated / Refuted Claims**: {hallucinated_claims}\n",
            "## Claim-by-Claim Verification Breakdown:\n"
        ]

        for idx, item in enumerate(claim_details, 1):
            verdict_icon = "❌ [HALLUCINATION]" if item["verdict"] == "REFUTES" else ("✅ [VERIFIED]" if item["verdict"] == "SUPPORTS" else "⚠️ [UNVERIFIED]")
            report.append(f"### Claim #{idx}: {item['claim_text']}")
            report.append(f"- **Verdict**: {verdict_icon}")
            report.append(f"- **Confidence**: {round(item['confidence_score'] * 100, 1)}%")
            report.append(f"- **Clinical Domain**: {item.get('category', 'General Medical')}")
            report.append(f"- **Explanation**: {item['explanation']}\n")

        return "\n".join(report)

explainability_engine = ExplainableAIEngine()
