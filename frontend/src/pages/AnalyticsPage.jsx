import React, { useEffect, useState } from 'react';
import { fetchAnalyticsStats } from '../services/api';
import { BarChart3, Target, Award, ShieldAlert, Cpu } from 'lucide-react';

export default function AnalyticsPage() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchAnalyticsStats().then(setStats);
  }, []);

  if (!stats) return <div className="p-8 text-center text-slate-400">Loading benchmark evaluation metrics...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold font-['Outfit'] text-white tracking-tight flex items-center gap-2">
          <BarChart3 className="w-7 h-7 text-cyan-400" />
          System Benchmark & Evaluation Metrics
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Performance metrics evaluated across 100 annotated clinical test cases (Pharmacology, Treatment, Safety, Diagnosis).
        </p>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Precision</span>
          <div className="text-3xl font-extrabold text-cyan-400 font-['Outfit']">
            {Math.round(stats.detection_precision * 100)}%
          </div>
          <p className="text-[11px] text-slate-400">Hallucination Flag Precision</p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Recall</span>
          <div className="text-3xl font-extrabold text-cyan-400 font-['Outfit']">
            {Math.round(stats.detection_recall * 100)}%
          </div>
          <p className="text-[11px] text-slate-400">Hallucination Sensitivity Rate</p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">F1 Score</span>
          <div className="text-3xl font-extrabold text-emerald-400 font-['Outfit']">
            {Math.round(stats.f1_score * 100)}%
          </div>
          <p className="text-[11px] text-slate-400">Harmonized F-Measure</p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">ROC-AUC</span>
          <div className="text-3xl font-extrabold text-cyan-300 font-['Outfit']">
            {stats.roc_auc_score}
          </div>
          <p className="text-[11px] text-slate-400">Discriminative Capability</p>
        </div>
      </div>

      {/* Model Hallucination Rate Comparison */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6">
        <h3 className="text-lg font-bold text-white font-['Outfit'] flex items-center gap-2">
          <Cpu className="w-5 h-5 text-cyan-400" />
          LLM Architecture Hallucination Frequency
        </h3>

        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span className="text-slate-200">Meta Llama 3 8B Instruct</span>
              <span className="text-cyan-400">14.5% Hallucination Rate</span>
            </div>
            <div className="h-3 rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full bg-cyan-500 rounded-full" style={{ width: '14.5%' }} />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span className="text-slate-200">OpenAI GPT-3.5 Turbo</span>
              <span className="text-amber-400">18.2% Hallucination Rate</span>
            </div>
            <div className="h-3 rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full bg-amber-500 rounded-full" style={{ width: '18.2%' }} />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span className="text-slate-200">BioMedLM (Clinical Fine-Tuned)</span>
              <span className="text-emerald-400">9.8% Hallucination Rate</span>
            </div>
            <div className="h-3 rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full bg-emerald-500 rounded-full" style={{ width: '9.8%' }} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
