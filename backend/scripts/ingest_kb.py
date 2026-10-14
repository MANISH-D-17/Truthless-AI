import os
import json
import chromadb
from chromadb.utils import embedding_functions

# Sample trusted healthcare knowledge documents
MEDICAL_KNOWLEDGE_DOCUMENTS = [
    {
        "id": "doc_who_ivermectin_2023",
        "title": "WHO Therapeutics and COVID-19 Living Guideline",
        "source_organization": "World Health Organization (WHO)",
        "domain": "Infectious Diseases / Pharmacology",
        "url": "https://www.who.int/publications/i/item/WHO-2019-nCoV-therapeutics-2023.1",
        "evidence_level": "High (WHO Official Living Guideline)",
        "content": (
            "WHO advises against the use of ivermectin for the treatment of COVID-19 outside of randomized controlled clinical trials. "
            "This recommendation applies to patients with any disease severity and any duration of symptoms. "
            "A systematic review of 16 randomized controlled trials involving 2,407 participants demonstrated low-certainty evidence of no reduction in mortality or hospital admission. "
            "High doses of ivermectin can lead to adverse events including neurological toxicity, hypotension, and elevated liver enzymes."
        )
    },
    {
        "id": "doc_fda_hydroxychloroquine_2023",
        "title": "FDA Drug Safety Communication: Hydroxychloroquine Risks",
        "source_organization": "U.S. Food and Drug Administration (FDA)",
        "domain": "Pharmacology & Safety",
        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/",
        "evidence_level": "High (FDA Regulatory Notice)",
        "content": (
            "The FDA revoked the Emergency Use Authorization (EUA) for hydroxychloroquine and chloroquine to treat COVID-19. "
            "Phase III clinical trials demonstrated no efficacy in reducing mortality or accelerating clinical recovery. "
            "Hydroxychloroquine is associated with severe cardiac side effects including QT interval prolongation, ventricular tachycardia, and severe hypoglycemia."
        )
    },
    {
        "id": "doc_ada_metformin_2024",
        "title": "ADA Standards of Care in Diabetes — 2024 Guidelines",
        "source_organization": "American Diabetes Association (ADA)",
        "domain": "Endocrinology & Metabolism",
        "url": "https://diabetesjournals.org/care",
        "evidence_level": "High (ADA Clinical Practice Standard)",
        "content": (
            "Metformin is the first-line pharmacologic therapy for adults with newly diagnosed Type 2 Diabetes Mellitus with adequate renal function. "
            "Initial dosage is typically 500 mg orally once or twice daily with meals, escalated up to 2000 mg daily. "
            "Metformin reduces hepatic gluconeogenesis and increases peripheral insulin sensitivity without inducing hypoglycemia. "
            "Metformin should be withheld in severe renal impairment (eGFR < 30 mL/min/1.73 m²) due to risk of lactic acidosis."
        )
    },
    {
        "id": "doc_cdc_pneumonia_2023",
        "title": "CDC Guidelines for Outpatient Pneumonia Management",
        "source_organization": "Centers for Disease Control and Prevention (CDC)",
        "domain": "Pulmonology & Infectious Diseases",
        "url": "https://www.cdc.gov/antibiotic-use/",
        "evidence_level": "High (CDC Guidelines)",
        "content": (
            "For outpatient adults with community-acquired pneumonia without comorbidities or risk factors for antibiotic-resistant pathogens, "
            "amoxicillin 1 g orally three times daily for 5 to 7 days is recommended as first-line empiric antibiotic therapy. "
            "Alternative regimens for penicillin-allergic patients include doxycycline 100 mg twice daily or a respiratory fluoroquinolone."
        )
    },
    {
        "id": "doc_nih_hypertension_2024",
        "title": "NIH Guideline for First-Line Antihypertensive Therapy",
        "source_organization": "National Institutes of Health (NIH)",
        "domain": "Cardiology & Vascular Medicine",
        "url": "https://www.nhlbi.nih.gov/",
        "evidence_level": "High (NIH Benchmark)",
        "content": (
            "First-line agents for hypertension in non-Black patients include thiazide diuretics, calcium channel blockers (CCBs), "
            "and Angiotensin-Converting Enzyme (ACE) inhibitors such as Lisinopril 10 mg to 40 mg daily. "
            "ACE inhibitors reduce blood pressure by inhibiting angiotensin I conversion to angiotensin II, reducing systemic vascular resistance. "
            "Common adverse effects of Lisinopril include persistent dry cough, hyperkalemia, and angioedema."
        )
    }
]

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def run_ingestion():
    chroma_dir = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
    os.makedirs(chroma_dir, exist_ok=True)
    
    print(f"Connecting to ChromaDB at: {chroma_dir}")
    client = chromadb.PersistentClient(path=chroma_dir)
    
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    collection = client.get_or_create_collection(
        name="healthcare_knowledge_base",
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"}
    )
    
    documents = []
    metadatas = []
    ids = []
    
    count = 0
    for doc in MEDICAL_KNOWLEDGE_DOCUMENTS:
        chunks = chunk_text(doc["content"])
        for idx, chunk in enumerate(chunks):
            count += 1
            doc_id = f"{doc['id']}_chunk_{idx}"
            ids.append(doc_id)
            documents.append(chunk)
            metadatas.append({
                "title": doc["title"],
                "source_organization": doc["source_organization"],
                "domain": doc["domain"],
                "url": doc["url"],
                "evidence_level": doc["evidence_level"]
            })
            
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    
    print(f"Successfully ingested {count} healthcare evidence chunks into ChromaDB!")

if __name__ == "__main__":
    run_ingestion()
