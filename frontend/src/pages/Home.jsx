import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Sparkles, Database, BarChart3, ArrowRight, Cpu, FileCheck2, Activity } from 'lucide-react';

export default function Home() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">
      {/* Hero Section */}
      <div className="text-center space-y-6 max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold tracking-wide uppercase">
          <Sparkles className="w-3.5 h-3.5" /> Final Year B.Tech AI & Data Science Capstone Platform
        </div>
        <h1 className="text-4xl sm:text-6xl font-extrabold font-['Outfit'] text-white tracking-tight leading-tight">
          AI-Powered Healthcare <br />
          <span className="bg-gradient-to-r from-cyan-400 via-sky-300 to-blue-500 bg-clip-text text-transparent">
            Hallucination Detection & Verification
          </span>
        </h1>
        <p className="text-lg text-slate-300 max-w-2xl mx-auto font-light leading-relaxed">
          Detect, verify, and explain AI-generated medical claims in real time using BioBERT NER, LangChain RAG, ChromaDB vector retrieval, and NLI entailment scoring over trusted WHO/CDC/FDA/PubMed literature.
        </p>
        <div className="flex flex-wrap justify-center gap-4 pt-4">
          <Link
            to="/verify"
            className="px-6 py-3.5 rounded-xl font-semibold text-slate-950 bg-gradient-to-r from-cyan-400 to-blue-500 hover:from-cyan-300 hover:to-blue-400 transition-all shadow-lg shadow-cyan-500/25 flex items-center gap-2"
          >
            <ShieldCheck className="w-5 h-5 stroke-[2.5]" />
            Launch Live Verification Engine
          </Link>
          <Link
            to="/analytics"
            className="px-6 py-3.5 rounded-xl font-semibold text-slate-200 glass-panel hover:bg-slate-800/80 transition-all border border-slate-700 flex items-center gap-2"
          >
            <BarChart3 className="w-5 h-5 text-cyan-400" />
            View Benchmark Analytics
          </Link>
        </div>
      </div>

      {/* Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="glass-panel p-8 rounded-2xl border border-slate-800 space-y-4 hover:border-cyan-500/40 transition">
          <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Cpu className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold font-['Outfit'] text-white">BioBERT Clinical NER</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Decomposes multi-sentence LLM output into atomic medical assertions and extracts diseases, drugs, dosages, and contraindications.
          </p>
        </div>

        <div className="glass-panel p-8 rounded-2xl border border-slate-800 space-y-4 hover:border-cyan-500/40 transition">
          <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Database className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold font-['Outfit'] text-white">ChromaDB RAG Corpora</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Multi-stage vector search across peer-reviewed WHO, CDC, FDA, and PubMed clinical practice guidelines.
          </p>
        </div>

        <div className="glass-panel p-8 rounded-2xl border border-slate-800 space-y-4 hover:border-cyan-500/40 transition">
          <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <FileCheck2 className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold font-['Outfit'] text-white">NLI Fact Verification</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Cross-Encoder DeBERTa-v3 Natural Language Inference assigns per-claim Entailment, Contradiction, and Neutral stance labels.
          </p>
        </div>
      </div>

      {/* System Architecture Pipeline */}
      <div className="glass-panel p-8 rounded-3xl border border-cyan-500/20 space-y-6">
        <div className="text-center space-y-2">
          <span className="text-xs font-mono text-cyan-400 uppercase tracking-widest">End-to-End Pipeline</span>
          <h2 className="text-2xl font-bold text-white font-['Outfit']">System Execution Architecture</h2>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-center text-xs">
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
            <span className="block font-bold text-cyan-400">1. Input Query</span>
            <span className="text-slate-400 text-[11px]">User prompt + LLM medical answer</span>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
            <span className="block font-bold text-cyan-400">2. Claim Extraction</span>
            <span className="text-slate-400 text-[11px]">Clause splitting & sentence filter</span>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
            <span className="block font-bold text-cyan-400">3. RAG Retrieval</span>
            <span className="text-slate-400 text-[11px]">ChromaDB top-k evidence match</span>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
            <span className="block font-bold text-cyan-400">4. NLI Engine</span>
            <span className="text-slate-400 text-[11px]">Entailment vs Contradiction</span>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1 col-span-2 md:col-span-1">
            <span className="block font-bold text-cyan-400">5. XAI Audit Report</span>
            <span className="text-slate-400 text-[11px]">Confidence score & heatmaps</span>
          </div>
        </div>
      </div>
    </div>
  );
}
