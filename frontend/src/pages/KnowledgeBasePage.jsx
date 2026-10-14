import React, { useEffect, useState } from 'react';
import { fetchKnowledgeSources } from '../services/api';
import { Database, Search, ExternalLink, ShieldCheck, FileText } from 'lucide-react';

export default function KnowledgeBasePage() {
  const [sources, setSources] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    fetchKnowledgeSources().then(setSources);
  }, []);

  const filteredSources = sources.filter(s =>
    s.title.toLowerCase().includes(filter.toLowerCase()) ||
    s.source_organization.toLowerCase().includes(filter.toLowerCase()) ||
    s.domain.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold font-['Outfit'] text-white tracking-tight flex items-center gap-2">
          <Database className="w-7 h-7 text-cyan-400" />
          Indexed Healthcare Knowledge Base Corpora
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          ChromaDB vector collection stores peer-reviewed clinical guidelines from WHO, CDC, FDA, NIH, and PubMed.
        </p>
      </div>

      {/* Search Filter */}
      <div className="relative max-w-md">
        <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter guidelines by org, title, domain..."
          className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-cyan-400"
        />
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredSources.map((s) => (
          <div key={s.id} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 hover:border-cyan-500/30 transition">
            <div className="flex items-start justify-between">
              <span className="text-xs font-semibold px-2.5 py-1 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                {s.source_organization}
              </span>
              <span className="text-xs font-mono text-slate-400">{s.publication_year}</span>
            </div>

            <div>
              <h3 className="text-lg font-bold text-white font-['Outfit']">{s.title}</h3>
              <p className="text-xs text-slate-400 mt-1">Domain: {s.domain}</p>
            </div>

            <div className="flex items-center justify-between text-xs pt-3 border-t border-slate-800 text-slate-400 font-mono">
              <span className="flex items-center gap-1">
                <FileText className="w-3.5 h-3.5 text-cyan-400" /> {s.chunks_count} Vector Chunks
              </span>
              <span className="text-emerald-400 flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5" /> Trusted Authority
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
