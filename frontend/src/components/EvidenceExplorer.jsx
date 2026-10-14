import React from 'react';
import { ExternalLink, BookOpen, Layers, Check, X, HelpCircle } from 'lucide-react';

export default function EvidenceExplorer({ claim }) {
  if (!claim) {
    return (
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 text-center text-slate-400 text-sm">
        Select an extracted claim from the list to view retrieved RAG evidence passages and NLI scores.
      </div>
    );
  }

  const evidences = claim.evidences || [];

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-5">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-cyan-400" />
          RAG Evidence & NLI Verification Inspector
        </h3>
        <span className="text-xs font-mono text-cyan-400 bg-cyan-500/10 px-2.5 py-1 rounded border border-cyan-500/20">
          NLI Entailment: {Math.round((claim.entailment_score || 0) * 100)}%
        </span>
      </div>

      {/* Selected Claim Explanation Box */}
      <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-700/60 space-y-2">
        <div className="text-xs font-semibold text-slate-400">Clinical Explanation & XAI Audit:</div>
        <p className="text-xs text-slate-200 leading-relaxed font-sans whitespace-pre-line">
          {claim.explanation}
        </p>
      </div>

      {/* NLI Score Breakdown Bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-xs text-slate-400 font-medium">
          <span>NLI Stance Distribution</span>
          <span className="text-slate-300 font-mono">
            Support: {Math.round(claim.entailment_score * 100)}% | Refute: {Math.round(claim.contradiction_score * 100)}% | Neutral: {Math.round(claim.neutral_score * 100)}%
          </span>
        </div>
        <div className="flex h-2.5 rounded-full overflow-hidden bg-slate-800">
          <div style={{ width: `${claim.entailment_score * 100}%` }} className="bg-emerald-500" title="Entailment / Support" />
          <div style={{ width: `${claim.contradiction_score * 100}%` }} className="bg-rose-500" title="Contradiction / Refute" />
          <div style={{ width: `${claim.neutral_score * 100}%` }} className="bg-amber-500" title="Neutral / Unverifiable" />
        </div>
      </div>

      {/* Retrieved Evidence Excerpts */}
      <div className="space-y-3 pt-2">
        <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <Layers className="w-3.5 h-3.5 text-cyan-400" />
          Retrieved Clinical Evidence ({evidences.length})
        </h4>

        {evidences.length === 0 ? (
          <p className="text-xs text-slate-500 italic">No matching evidence found in ChromaDB vector index.</p>
        ) : (
          evidences.map((ev, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
              <div className="flex items-start justify-between gap-2">
                <div>
                  <span className="text-xs font-bold text-cyan-300 flex items-center gap-1">
                    {ev.source_name}
                  </span>
                  <h5 className="text-xs text-slate-300 font-medium mt-0.5">{ev.title}</h5>
                </div>
                {ev.url && (
                  <a
                    href={ev.url}
                    target="_blank"
                    rel="noreferrer"
                    className="p-1 rounded text-slate-400 hover:text-cyan-400 hover:bg-slate-800 transition"
                    title="View Original Source"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>

              <p className="text-xs text-slate-300 leading-relaxed italic bg-slate-900/40 p-2.5 rounded border border-slate-800">
                "{ev.excerpt}"
              </p>

              <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1 font-mono">
                <span>Vector Cosine Sim: <strong className="text-slate-200">{ev.similarity_score}</strong></span>
                <span className="text-cyan-400/80">{ev.evidence_level}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
