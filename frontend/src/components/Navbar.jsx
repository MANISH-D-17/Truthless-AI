import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ShieldCheck, Database, BarChart3, Home, Sparkles } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-cyan-500/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
            <ShieldCheck className="w-6 h-6 text-slate-950 stroke-[2.5]" />
          </div>
          <div>
            <span className="font-['Outfit'] font-bold text-xl tracking-tight text-white flex items-center gap-1.5">
              MediVerify <span className="text-cyan-400 font-semibold text-xs px-2 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30">AI RAG v1.0</span>
            </span>
            <p className="text-[10px] text-slate-400 -mt-1 font-medium">Healthcare Hallucination Verification Engine</p>
          </div>
        </Link>

        <nav className="flex items-center space-x-1 sm:space-x-2">
          <Link
            to="/"
            className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
              isActive('/') ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30' : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <Home className="w-4 h-4" />
            <span>Dashboard</span>
          </Link>
          <Link
            to="/verify"
            className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
              isActive('/verify') ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30' : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <Sparkles className="w-4 h-4 text-cyan-400" />
            <span>Verify LLM Claim</span>
          </Link>
          <Link
            to="/knowledge"
            className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
              isActive('/knowledge') ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30' : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <Database className="w-4 h-4" />
            <span>Knowledge Corpora</span>
          </Link>
          <Link
            to="/analytics"
            className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
              isActive('/analytics') ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30' : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span>Benchmark Analytics</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}
