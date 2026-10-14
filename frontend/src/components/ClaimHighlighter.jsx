import React, { useState } from 'react';
import { AlertTriangle, CheckCircle2, HelpCircle, Activity } from 'lucide-react';

function renderInlineClaimText(claimText, entities = []) {
  if (!entities || entities.length === 0) {
    return <span>"{claimText}"</span>;
  }

  const validEntities = entities
    .filter(
      (e) =>
        typeof e.start === 'number' &&
        typeof e.end === 'number' &&
        e.start >= 0 &&
        e.end <= claimText.length &&
        e.start <= e.end
    )
    .sort((a, b) => a.start - b.start || (b.end - b.start) - (a.end - a.start));

  const nonOverlapping = [];
  let lastEnd = -1;
  for (const ent of validEntities) {
    if (ent.start >= lastEnd) {
      nonOverlapping.push(ent);
      lastEnd = ent.end;
    }
  }

  const parts = [];
  let cursor = 0;

  nonOverlapping.forEach((ent, idx) => {
    if (ent.start > cursor) {
      parts.push(
        <span key={`txt-${cursor}`}>{claimText.slice(cursor, ent.start)}</span>
      );
    }

    const labelUpper = (ent.label || '').toUpperCase();
    let styleClass = 'bg-slate-500/20 text-slate-300 border-slate-500/40';
    if (labelUpper === 'DRUG') {
      styleClass = 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40';
    } else if (labelUpper === 'DISEASE') {
      styleClass = 'bg-rose-500/20 text-rose-300 border-rose-500/40';
    } else if (labelUpper === 'DOSAGE') {
      styleClass = 'bg-amber-500/20 text-amber-300 border-amber-500/40';
    } else if (labelUpper === 'TREATMENT') {
      styleClass = 'bg-violet-500/20 text-violet-300 border-violet-500/40';
    }

    parts.push(
      <mark
        key={`ent-${idx}-${ent.start}`}
        className={`inline-block px-1.5 py-0.5 rounded border text-xs font-semibold mx-0.5 align-baseline font-mono ${styleClass}`}
        title={`${ent.label}: ${ent.text}`}
      >
        {claimText.slice(ent.start, ent.end)}
      </mark>
    );

    cursor = ent.end;
  });

  if (cursor < claimText.length) {
    parts.push(
      <span key={`txt-end-${cursor}`}>{claimText.slice(cursor)}</span>
    );
  }

  return <span>"{parts}"</span>;
}

const FILTER_TABS = [
  { key: 'ALL', label: 'All' },
  { key: 'VERIFIED', label: 'Verified' },
  { key: 'REFUTED', label: 'Refuted' },
  { key: 'UNVERIFIED', label: 'Unverified' }
];

export default function ClaimHighlighter({ claims = [], selectedClaimId, onSelectClaim }) {
  const [filter, setFilter] = useState('ALL');

  if (!claims || claims.length === 0) {
    return (
      <div className="p-6 text-center text-slate-400 bg-slate-900/40 rounded-xl border border-slate-800">
        No claims extracted yet. Run verification on an LLM response.
      </div>
    );
  }

  const totalCount = claims.length;
  const verifiedCount = claims.filter((c) => c.verdict === 'SUPPORTS').length;
  const refutedCount = claims.filter((c) => c.verdict === 'REFUTES').length;
  const unverifiedCount = claims.filter(
    (c) => c.verdict !== 'SUPPORTS' && c.verdict !== 'REFUTES'
  ).length;

  const counterText = `${totalCount} ${totalCount === 1 ? 'claim' : 'claims'} - ${verifiedCount} verified - ${refutedCount} refuted - ${unverifiedCount} unverified`;

  const filteredClaims = claims.filter((c) => {
    if (filter === 'VERIFIED') return c.verdict === 'SUPPORTS';
    if (filter === 'REFUTED') return c.verdict === 'REFUTES';
    if (filter === 'UNVERIFIED') return c.verdict !== 'SUPPORTS' && c.verdict !== 'REFUTES';
    return true;
  });

  return (
    <div className="space-y-4">
      {/* Header and Counter */}
      <div className="space-y-2">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <h3 className="text-xs uppercase tracking-wider font-semibold text-slate-400 flex items-center gap-2">
            <Activity className="w-4 h-4 text-cyan-400" />
            Extracted Medical Claims & BioBERT Entity Inspector
          </h3>

          {/* Filter Tabs */}
          <div className="flex items-center gap-1 p-1 bg-slate-900/80 rounded-lg border border-slate-800 w-fit">
            {FILTER_TABS.map((tab) => (
              <button
                key={tab.key}
                type="button"
                onClick={() => setFilter(tab.key)}
                className={`px-2.5 py-1 text-xs rounded-md font-medium transition ${
                  filter === tab.key
                    ? 'bg-slate-800 text-cyan-300 shadow-sm border border-slate-700'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <p className="text-xs font-mono text-slate-400">
          {counterText}
        </p>
      </div>

      {/* Claims List */}
      <div className="space-y-3">
        {filteredClaims.length === 0 ? (
          <div className="p-6 text-center text-xs text-slate-400 bg-slate-900/40 rounded-xl border border-slate-800">
            No claims found for "{filter.toLowerCase()}" filter.
          </div>
        ) : (
          filteredClaims.map((c, index) => {
            const isSelected = selectedClaimId === c.claim_id;
            const isRefuted = c.verdict === 'REFUTES';
            const isSupported = c.verdict === 'SUPPORTS';

            let statusBg = isRefuted
              ? 'bg-rose-950/40 border-rose-500/40 hover:border-rose-400'
              : isSupported
              ? 'bg-emerald-950/40 border-emerald-500/40 hover:border-emerald-400'
              : 'bg-amber-950/40 border-amber-500/40 hover:border-amber-400';

            let statusBadge = isRefuted ? (
              <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/40">
                <AlertTriangle className="w-3.5 h-3.5" /> Hallucinated / Refuted
              </span>
            ) : isSupported ? (
              <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                <CheckCircle2 className="w-3.5 h-3.5" /> Verified Claim
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40">
                <HelpCircle className="w-3.5 h-3.5" /> Unverified / Caution
              </span>
            );

            return (
              <div
                key={c.claim_id}
                onClick={() => onSelectClaim && onSelectClaim(c)}
                className={`p-4 rounded-xl border transition-all cursor-pointer ${statusBg} ${
                  isSelected ? 'ring-2 ring-cyan-400 shadow-lg' : ''
                }`}
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <span className="text-xs font-mono text-slate-400">Claim #{index + 1}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded-full bg-slate-800/90 text-slate-300 border border-slate-700">
                      {Math.round((c.confidence_score || 0) * 100)}%
                    </span>
                    {statusBadge}
                  </div>
                </div>

                <p className="text-sm text-slate-100 font-medium leading-relaxed mb-3">
                  {renderInlineClaimText(c.claim_text, c.entities)}
                </p>

                {/* BioBERT Medical Entities */}
                {c.entities && c.entities.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 pt-2 border-t border-slate-800/80">
                    <span className="text-[11px] text-slate-400 mr-1 self-center font-mono">Entities:</span>
                    {c.entities.map((ent, idx) => (
                      <span
                        key={idx}
                        className="text-[11px] font-semibold px-2 py-0.5 rounded bg-slate-800/90 text-cyan-300 border border-cyan-500/30 font-mono"
                      >
                        {ent.text} <span className="opacity-60 text-[9px] font-sans">[{ent.label}]</span>
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
