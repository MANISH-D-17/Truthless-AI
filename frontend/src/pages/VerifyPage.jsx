import React, { useState, useRef } from 'react';
import { verifyResponse } from '../services/api';
import ClaimHighlighter from '../components/ClaimHighlighter';
import ConfidenceRadar from '../components/ConfidenceRadar';
import EvidenceExplorer from '../components/EvidenceExplorer';
import { Sparkles, RefreshCw, AlertCircle, CheckCircle2, Play } from 'lucide-react';

const SAMPLE_PROMPTS = [
  {
    label: "Sample 1: Hallucinated Ivermectin Claim",
    query: "Is Ivermectin approved by WHO for treating COVID-19?",
    response: "Ivermectin is an effective first-line cure for COVID-19 approved by WHO in 12 mg daily dosages."
  },
  {
    label: "Sample 2: Verified Metformin Diabetes Dosage",
    query: "What is the recommended initial dose of Metformin for Type 2 Diabetes?",
    response: "Metformin is recommended as first-line therapy for type 2 diabetes starting at 500 mg daily with meals."
  },
  {
    label: "Sample 3: Refuted Hydroxychloroquine Assertion",
    query: "Can Hydroxychloroquine cure COVID-19 according to FDA?",
    response: "FDA strongly recommends Hydroxychloroquine as a safe cure for all hospitalized COVID-19 patients."
  }
];

export default function VerifyPage() {
  const [query, setQuery] = useState('');
  const [llmResponse, setLlmResponse] = useState('');
  const [llmModel, setLlmModel] = useState('Llama-3-8B-Instruct');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [selectedClaim, setSelectedClaim] = useState(null);
  const resultsRef = useRef(null);

  const handleVerify = async (e) => {
    if (e) e.preventDefault();
    if (!llmResponse.trim()) return;

    setLoading(true);
    setResult(null);
    setSelectedClaim(null);

    const data = await verifyResponse(query, llmResponse, llmModel);
    setResult(data);
    if (data && data.claims_verification && data.claims_verification.length > 0) {
      setSelectedClaim(data.claims_verification[0]);
    }
    setLoading(false);

    setTimeout(() => {
      resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  };

  const loadSample = (sample) => {
    setQuery(sample.query);
    setLlmResponse(sample.response);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-extrabold font-['Outfit'] text-white tracking-tight flex items-center gap-2">
          <Sparkles className="w-7 h-7 text-cyan-400" />
          Interactive Hallucination Detection Console
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Paste any AI-generated medical statement below to run real-time RAG fact verification.
        </p>
      </div>

      {/* Preset Benchmarks */}
      <div className="flex flex-wrap items-center gap-2 pt-1">
        <span className="text-xs text-slate-400 font-medium">Preset Test Cases:</span>
        {SAMPLE_PROMPTS.map((sample, idx) => (
          <button
            key={idx}
            onClick={() => loadSample(sample)}
            className="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-cyan-300 border border-slate-700 transition flex items-center gap-1"
          >
            <Play className="w-3 h-3 text-cyan-400" />
            {sample.label}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <form onSubmit={handleVerify} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2 space-y-1">
            <label className="text-xs font-semibold text-slate-300">Healthcare User Query (Optional)</label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. Is Ivermectin approved for COVID-19 treatment?"
              className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-300">LLM Source Engine</label>
            <select
              value={llmModel}
              onChange={(e) => setLlmModel(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-100 text-sm focus:outline-none focus:border-cyan-400"
            >
              <option value="Llama-3-8B-Instruct">Meta Llama 3 8B Instruct</option>
              <option value="GPT-3.5-Turbo">OpenAI GPT-3.5 Turbo</option>
              <option value="BioMedLM">BioMedLM Clinical Specialization</option>
            </select>
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-xs font-semibold text-slate-300">AI-Generated Medical Response / Claim Text</label>
          <textarea
            rows={4}
            value={llmResponse}
            onChange={(e) => setLlmResponse(e.target.value)}
            placeholder="Paste the LLM generated medical response here..."
            className="w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400 font-sans"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3.5 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-blue-500 hover:from-cyan-300 hover:to-blue-400 transition shadow-lg shadow-cyan-500/20 flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <RefreshCw className="w-5 h-5 animate-spin" />
              Running BioBERT NER & ChromaDB Vector RAG Verification...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5 fill-slate-950" />
              Verify Healthcare Response
            </>
          )}
        </button>
      </form>

      {/* Results Workspace */}
      {result && (
        <div ref={resultsRef} className="space-y-6 animate-in fade-in duration-500 scroll-mt-6">
          {/* Demo Mode Banner */}
          {result.is_demo_mode && (
            <div className="flex items-center gap-2.5 px-4 py-2.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs sm:text-sm font-medium">
              <AlertCircle className="w-4 h-4 shrink-0 text-amber-400" />
              <span>Demo mode: backend not connected. Claims are analysed locally with a rule-based engine.</span>
            </div>
          )}

          {/* Top Level Confidence Bar */}
          <ConfidenceRadar
            overallScore={result.overall_confidence_score}
            hallucinationDetected={result.hallucination_detected}
            totalClaims={result.total_claims_count}
            hallucinatedCount={result.hallucinated_claims_count}
          />

          {/* Side-by-side Inspection Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <ClaimHighlighter
              claims={result.claims_verification}
              selectedClaimId={selectedClaim ? selectedClaim.claim_id : null}
              onSelectClaim={(claim) => setSelectedClaim(claim)}
            />

            <EvidenceExplorer claim={selectedClaim} />
          </div>
        </div>
      )}
    </div>
  );
}
