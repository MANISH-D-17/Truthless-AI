import re
from typing import List, Dict, Any
from app.core.config import settings

class BioBERTMedicalNER:
    """
    BioBERT & ClinicalBERT Named Entity Recognition (NER) Service:
    Identifies clinical entities (Diseases, Medications, Treatments, Dosages, Symptoms)
    from extracted medical claims.
    """
    def __init__(self):
        self.pipeline = None
        self.initialized = False
        
        # Clinical dictionary vocabulary for rapid entity tagging fallback
        self.known_drugs = [
            "ivermectin", "hydroxychloroquine", "remdesivir", "paxlovid", "amoxicillin",
            "metformin", "lisinopril", "atorvastatin", "albuterol", "dexamethasone",
            "semaglutide", "ibuprofen", "acetaminophen", "aspirin", "warfarin", "pembrolizumab"
        ]
        self.known_diseases = [
            "covid-19", "coronavirus", "hypertension", "type 2 diabetes", "malaria",
            "pneumonia", "asthma", "breast cancer", "lung cancer", "myocardial infarction",
            "stroke", "alzheimer's", "tuberculosis", "rheumatoid arthritis", "influenza"
        ]
        self.known_treatments = [
            "chemotherapy", "radiation therapy", "intubation", "dialysis", "immunotherapy",
            "monoclonal antibody", "supplementation", "antiviral therapy", "angioplasty"
        ]

    def _lazy_init(self):
        if not self.initialized:
            try:
                from transformers import pipeline
                self.pipeline = pipeline("ner", model=settings.BIOBERT_NER_MODEL, aggregation_strategy="simple")
                self.initialized = True
                print(f"Loaded BioBERT NER Model: {settings.BIOBERT_NER_MODEL}")
            except Exception as e:
                print(f"Warning: Could not load BioBERT model ({e}). Using dictionary rule-based NER engine.")
                self.pipeline = None
                self.initialized = True

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        self._lazy_init()
        entities = []

        if self.pipeline:
            try:
                ner_results = self.pipeline(text)
                for res in ner_results:
                    entities.append({
                        "text": res.get("word", ""),
                        "label": res.get("entity_group", "CLINICAL_ENTITY"),
                        "start": res.get("start", 0),
                        "end": res.get("end", 0)
                    })
                if entities:
                    return entities
            except Exception as e:
                print(f"BioBERT pipeline inference error: {e}")

        # Rule-based fallback entity extractor
        text_lower = text.lower()
        
        # 1. Drugs / Chemicals
        for drug in self.known_drugs:
            for match in re.finditer(r'\b' + re.escape(drug) + r'\b', text_lower):
                entities.append({
                    "text": text[match.start():match.end()],
                    "label": "DRUG",
                    "start": match.start(),
                    "end": match.end()
                })

        # 2. Diseases / Conditions
        for disease in self.known_diseases:
            for match in re.finditer(r'\b' + re.escape(disease) + r'\b', text_lower):
                entities.append({
                    "text": text[match.start():match.end()],
                    "label": "DISEASE",
                    "start": match.start(),
                    "end": match.end()
                })

        # 3. Treatments & Procedures
        for treatment in self.known_treatments:
            for match in re.finditer(r'\b' + re.escape(treatment) + r'\b', text_lower):
                entities.append({
                    "text": text[match.start():match.end()],
                    "label": "TREATMENT",
                    "start": match.start(),
                    "end": match.end()
                })

        # 4. Dosage Patterns (e.g. 50mg, 10 mg/kg, twice daily)
        dosage_matches = re.finditer(r'\b\d+(\.\d+)?\s*(mg|g|mcg|ml|mg/kg|units|daily|twice daily|once daily)\b', text_lower)
        for match in dosage_matches:
            entities.append({
                "text": text[match.start():match.end()],
                "label": "DOSAGE",
                "start": match.start(),
                "end": match.end()
            })

        return entities

medical_ner = BioBERTMedicalNER()
