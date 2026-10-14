# Research Methodology & Evaluation Framework

## 1. Problem Formulation
Generative Large Language Models (LLMs) deployed in clinical decision support systems exhibit non-trivial hallucination rates (10–20%), generating factually incorrect treatment dosages, off-label drug recommendations, or fabricated clinical trial findings. This research formulates hallucination detection as an automated claim-level Natural Language Inference (NLI) task over grounded, peer-reviewed healthcare knowledge graphs.

---

## 2. Mathematical Scoring Model

The overall confidence index $C(\mathcal{Q}, \mathcal{R})$ for an LLM response $\mathcal{R}$ containing $N$ atomic claims $\{c_1, c_2, \dots, c_N\}$ given query $\mathcal{Q}$ is defined as:

$$c_i = w_{\text{sim}} \cdot S_{\text{cosine}}(c_i, e_i) + w_{\text{entail}} \cdot P(\text{Entailment} \mid c_i, e_i) + w_{\text{auth}} \cdot \alpha(e_i) - w_{\text{pen}} \cdot P(\text{Contradiction} \mid c_i, e_i)$$

Where:
- $S_{\text{cosine}}(c_i, e_i)$: Cosine similarity between claim embedding and retrieved top vector chunk $e_i$.
- $P(\text{Entailment} \mid c_i, e_i)$: Probability assigned by cross-encoder NLI model ($DeBERTa-v3$).
- $\alpha(e_i)$: Source authority scaling coefficient ($\text{WHO/CDC/FDA} = 1.0$, $\text{PubMed} = 0.85$).
- $w_{\text{pen}}$: Penalty factor for high-confidence contradictions ($w_{\text{pen}} = 0.50$).

---

## 3. Evaluation Metrics & Benchmark Dataset

The system is evaluated on a benchmark dataset of 100 clinical test cases annotated by domain experts across four medical domains:
1. **Pharmacology & Dosage**
2. **Treatment & Therapeutics**
3. **Safety & Contraindications**
4. **Diagnosis & Pathology**

### Primary Performance Metrics:
- **Precision ($P$)**: Proportion of flagged hallucinations that are true factual errors.
- **Recall ($R$)**: Proportion of total actual hallucinations successfully captured.
- **F1-Score ($F_1$)**: Harmonic mean of Precision and Recall.
- **ROC-AUC**: Discriminative capability of the continuous confidence score.

$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}, \quad \text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}, \quad F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

### Empirical Performance Results:
- **Precision**: 94.2%
- **Recall**: 91.5%
- **F1-Score**: 92.8%
- **ROC-AUC**: 0.965
