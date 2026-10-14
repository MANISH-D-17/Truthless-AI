import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import VerifyPage from './pages/VerifyPage';
import KnowledgeBasePage from './pages/KnowledgeBasePage';
import AnalyticsPage from './pages/AnalyticsPage';

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#0b132b] text-slate-100 font-['Inter',sans-serif] flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/verify" element={<VerifyPage />} />
            <Route path="/knowledge" element={<KnowledgeBasePage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
          </Routes>
        </main>
        <footer className="border-t border-slate-800/80 py-6 text-center text-xs text-slate-500 font-mono">
          AI-Powered Healthcare Hallucination Detection & Verification Platform — B.Tech Capstone 2026
        </footer>
      </div>
    </Router>
  );
}
