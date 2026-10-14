import json
import os
import sys

# Ensure backend path in python module lookup
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.claim_extractor import claim_extractor
from app.services.vector_store import vector_store
from app.services.verifier import verifier
from app.services.scoring import scoring_engine

def evaluate_system():
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "test_dataset_100.json")
    if not os.path.exists(dataset_path):
        print(f"Error: Test dataset not found at {dataset_path}")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    print(f"Running System Evaluation over {len(test_cases)} Healthcare Test Cases...")
    
    tp = 0  # True Positives: Correctly identified Hallucinations / Refutations
    fp = 0  # False Positives: Falsely flagged valid claim as Hallucination
    tn = 0  # True Negatives: Correctly identified Valid / Supported Claim
    fn = 0  # False Negatives: Missed Hallucination

    for tc in test_cases:
        query = tc["query"]
        llm_resp = tc["llm_response"]
        gt_claims = tc.get("ground_truth_claims", [])

        # Extract & verify
        claims = claim_extractor.extract_claims(llm_resp)
        for idx, item in enumerate(claims):
            c_text = item["claim_text"]
            evidences = vector_store.search_evidence(c_text, top_k=3)
            verdict_res = verifier.verify_claim_against_evidences(c_text, evidences)
            pred_verdict = verdict_res["verdict"]

            # Match ground truth
            gt_label = gt_claims[idx]["label"] if idx < len(gt_claims) else "NOT_ENOUGH_INFO"

            if gt_label == "REFUTES":
                if pred_verdict == "REFUTES":
                    tp += 1
                else:
                    fn += 1
            elif gt_label == "SUPPORTS":
                if pred_verdict == "SUPPORTS":
                    tn += 1
                elif pred_verdict == "REFUTES":
                    fp += 1
                else:
                    tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 1.0

    print("\n================ SYSTEM EVALUATION METRICS ================")
    print(f"Total Evaluated Claims: {tp + tn + fp + fn}")
    print(f"True Positives (Detected Hallucinations): {tp}")
    print(f"False Positives: {fp}")
    print(f"True Negatives (Verified Claims): {tn}")
    print(f"False Negatives (Missed Hallucinations): {fn}")
    print(f"Precision: {round(precision * 100, 2)}%")
    print(f"Recall: {round(recall * 100, 2)}%")
    print(f"F1-Score: {round(f1 * 100, 2)}%")
    print(f"Accuracy: {round(accuracy * 100, 2)}%")
    print("==========================================================")

if __name__ == "__main__":
    evaluate_system()
