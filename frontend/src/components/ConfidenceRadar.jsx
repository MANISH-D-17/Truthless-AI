import React from 'react';
import { Gauge, ShieldAlert, ShieldCheck } from 'lucide-react';

export default function ConfidenceRadar({ overallScore = 0.85, hallucinationDetected = false, totalClaims = 0, hallucinatedCount = 0 }) {
  const percentage = Math.round(overallScore * 100);
  
  let scoreColor = percentage >= 80 ? 'text-emerald-400' : percentage >= 50 ? 'text-amber-400' : 'text-rose-400';
  let barColor = percentage >= 80 ? 'bg-emerald-500' : percentage >= 50 ? 'bg-amber-500' : 'bg-rose-500';

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
          <Gauge className="w-4 h-4 text-cyan-400" />
          Factual Confidence Radar
        </h3>
        {hallucinationDetected ? (
          <span className="flex items-center gap-1.5 text-xs font-bold text-rose-300 px-3 py-1 rounded-full bg-rose-500/20 border border-rose-500/40">
            <ShieldAlert className="w-4 h-4 text-rose-400" /> Clinical Hallucination Risk
          </span>
        ) : (
          <span className="flex items-center gap-1.5 text-xs font-bold text-emerald-300 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-500/40">
            <ShieldCheck className="w-4 h-4 text-emerald-400" /> Verified Evidence Level
          </span>
        )}
      </div>

      <div className="flex items-end justify-between">
        <div>
          <div className={`text-4xl font-extrabold font-['Outfit'] ${scoreColor}`}>
            {percentage}%
          </div>
          <p className="text-xs text-slate-400 mt-1">Overall Factual Accuracy Index</p>
        </div>

        <div className="text-right space-y-1">
          <div className="text-xs font-semibold text-slate-300">
            {totalClaims - hallucinatedCount} / {totalClaims} Verified Claims
          </div>
          <div className="text-[11px] text-slate-400 font-mono">
            Hallucinated: <span className="text-rose-400 font-bold">{hallucinatedCount}</span>
          </div>
        </div>
      </div>

      {/* Progress Meter Bar */}
      <div className="w-full bg-slate-800 rounded-full h-3 overflow-hidden p-0.5 border border-slate-700">
        <div
          className={`h-full rounded-full transition-all duration-700 ease-out ${barColor}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>

      <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800/80 text-center text-xs">
        <div className="p-2 rounded-lg bg-slate-900/50">
          <span className="block text-slate-400 text-[10px] uppercase font-semibold">ChromaDB RAG</span>
          <span className="font-bold text-cyan-300">Top-3 Matches</span>
        </div>
        <div className="p-2 rounded-lg bg-slate-900/50">
          <span className="block text-slate-400 text-[10px] uppercase font-semibold">NLI Engine</span>
          <span className="font-bold text-cyan-300">DeBERTa-v3</span>
        </div>
        <div className="p-2 rounded-lg bg-slate-900/50">
          <span className="block text-slate-400 text-[10px] uppercase font-semibold">Corpora</span>
          <span className="font-bold text-cyan-300">WHO / CDC / FDA</span>
        </div>
      </div>
    </div>
  );
}
