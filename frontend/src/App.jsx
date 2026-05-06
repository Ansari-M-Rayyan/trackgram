import React, { useState } from 'react';
import { 
  ShieldAlert, Search, Cpu, Share2, Eye, Terminal, 
  Download, AlertCircle, RefreshCcw, Briefcase, Hash
} from 'lucide-react';

const App = () => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const uploadedFile = e.target.files[0];
    if (!uploadedFile) return;
    setLoading(true);
    setReport(null);

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/analyze-file', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      
      if (data.error) {
        alert("Backend Logic Error: " + data.error);
      } else {
        setReport(data);
      }
    } catch (err) {
      alert("Network Error: Is main.py running?");
    } finally {
      setLoading(false);
    }
  };

  const resetInvestigation = () => {
    setReport(null);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0c] text-slate-300 font-mono p-4 md:p-10">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center border-b border-white/10 pb-8 mb-10">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tighter flex items-center gap-2 uppercase">
            <ShieldAlert className="text-red-500" /> TrackGram <span className="text-red-600 italic font-black">v2.0</span>
          </h1>
          <p className="text-[10px] text-slate-500 mt-2 uppercase tracking-[0.3em]">AI-Driven Forensic Intelligence Hub</p>
        </div>
        
        {report && (
          <div className="flex gap-4 mt-6 md:mt-0">
            <button onClick={resetInvestigation} className="flex items-center gap-2 border border-white/20 px-4 py-2 text-[10px] font-bold hover:bg-white/5 transition-all text-white">
              <RefreshCcw size={14} /> NEW_SCAN
            </button>
            <button onClick={() => window.print()} className="flex items-center gap-2 bg-white text-black px-4 py-2 text-[10px] font-bold hover:bg-red-600 hover:text-white transition-all">
              <Download size={14} /> EXPORT_CASE
            </button>
          </div>
        )}
      </div>

      <main className="max-w-6xl mx-auto">
        {!report ? (
          <div className="h-[450px] border-2 border-dashed border-white/5 rounded-2xl flex flex-col items-center justify-center bg-white/[0.01] transition-all hover:bg-white/[0.02] hover:border-white/10">
            <input type="file" id="dossier-upload" className="hidden" onChange={handleUpload} accept=".json" />
            <label htmlFor="dossier-upload" className="cursor-pointer group flex flex-col items-center">
              <div className="w-24 h-24 bg-white/5 rounded-full flex items-center justify-center group-hover:scale-110 group-hover:bg-red-500/10 transition-all border border-white/10">
                <Search className="text-slate-500 group-hover:text-red-500" size={40} />
              </div>
              <span className="mt-8 text-xs font-bold tracking-[0.4em] text-slate-500 group-hover:text-white uppercase">Upload Forensic Payload (JSON)</span>
            </label>
            {loading && (
              <div className="mt-12 text-center">
                <div className="flex items-center justify-center gap-4 mb-4">
                  <div className="w-2 h-2 bg-red-600 animate-bounce"></div>
                  <div className="w-2 h-2 bg-red-600 animate-bounce delay-100"></div>
                  <div className="w-2 h-2 bg-red-600 animate-bounce delay-200"></div>
                </div>
                <p className="text-[10px] text-red-500 font-black tracking-widest uppercase">Initializing Neural Engine & LLM Reasoning...</p>
              </div>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 animate-in fade-in slide-in-from-bottom-8 duration-1000">
            
            {/* LLM Intelligence Dossier */}
            <div className="lg:col-span-8 bg-[#111113] border border-white/10 p-10 rounded-lg shadow-2xl relative">
               <div className="absolute top-0 right-0 px-4 py-1 bg-red-600 text-[9px] font-black text-white uppercase tracking-widest">
                 Dossier Report
               </div>
               <h3 className="text-white text-xs font-bold mb-8 flex items-center gap-3 uppercase tracking-widest border-b border-white/5 pb-4">
                 <Terminal size={18} className="text-red-500" /> Forensic Intelligence Briefing
               </h3>
               
               <div className="text-lg leading-relaxed text-slate-200 font-serif whitespace-pre-wrap">
                 {report.forensics.report}
               </div>
               
               <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12 pt-8 border-t border-white/5">
                 <div className="bg-white/[0.02] p-5 border border-white/5 rounded">
                    <h4 className="text-[10px] text-red-500 uppercase mb-4 font-black flex items-center gap-2">
                      <Share2 size={14} /> Network Associates
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {report.network.mentions.length > 0 ? report.network.mentions.map((m, i) => (
                        <span key={i} className="text-[11px] bg-red-500/10 text-red-400 px-3 py-1.5 border border-red-500/20">{m}</span>
                      )) : <span className="text-[11px] text-slate-600">No associates detected.</span>}
                    </div>
                 </div>
                 
                 <div className="bg-white/[0.02] p-5 border border-white/5 rounded">
                    <h4 className="text-[10px] text-slate-400 uppercase mb-4 font-black flex items-center gap-2">
                      <Hash size={14} /> Thematic Topics
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {report.network.topics.length > 0 ? report.network.topics.map((t, i) => (
                        <span key={i} className="text-[11px] bg-white/5 text-slate-300 px-3 py-1.5 border border-white/10">{t}</span>
                      )) : <span className="text-[11px] text-slate-600">No topics detected.</span>}
                    </div>
                 </div>
               </div>
            </div>

            {/* Metrics Sidebar */}
            <div className="lg:col-span-4 space-y-8">
              
              {/* Legitimacy Score */}
              <div className="bg-[#111113] border border-white/10 p-8 rounded-lg text-center shadow-2xl relative group">
                <div className="absolute top-4 right-4 cursor-help text-slate-600 hover:text-white transition-colors">
                  <AlertCircle size={16} />
                  <span className="absolute hidden group-hover:block w-48 bg-black border border-white/20 p-3 text-[10px] text-left leading-tight right-0 top-6 z-50 rounded shadow-xl">
                    LEGITIMACY RATING: Evaluates follower-to-following ratios, verification status, and network isolation to determine if the profile exhibits authentic professional behavior.
                  </span>
                </div>

                <h3 className="text-[9px] text-slate-500 uppercase tracking-[0.3em] mb-6 font-bold">Profile Legitimacy Rating</h3>
                <div className={`text-7xl font-black mb-4 ${report.forensics.legitimacy_score < 50 ? 'text-red-600' : 'text-green-500'}`}>
                  {report.forensics.legitimacy_score}%
                </div>
                
                <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden mb-4">
                   <div className={`h-full transition-all duration-1000 ${report.forensics.legitimacy_score < 50 ? 'bg-red-600' : 'bg-green-500'}`} style={{width: `${report.forensics.legitimacy_score}%`}}></div>
                </div>

                <div className="space-y-2 mt-6 border-t border-white/5 pt-4 text-left">
                    <p className="text-[10px] text-white uppercase tracking-tighter flex justify-between">
                      Handle: <span className="text-slate-400 font-bold">{report.identity.handle}</span>
                    </p>
                    <p className="text-[10px] text-white uppercase tracking-tighter flex justify-between">
                      Status: <span className="text-red-500 font-black">{report.identity.status}</span>
                    </p>
                </div>
              </div>

              {/* Vision Recon */}
              <div className="bg-[#111113] border border-white/10 p-8 rounded-lg shadow-2xl">
                <h3 className="text-[9px] text-slate-500 uppercase tracking-[0.3em] mb-6 font-bold flex items-center gap-2">
                  <Eye size={14} /> Digital Environment Context
                </h3>
                <div className="space-y-3">
                  {report.forensics.environment.map((tag, i) => (
                    <div key={i} className="flex items-center gap-3 group">
                      <div className="w-1.5 h-1.5 bg-red-600 group-hover:scale-150 transition-all"></div>
                      <span className="text-xs font-black text-slate-300 group-hover:text-white transition-all">{tag}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Dynamic Hardware Status */}
              <div className="bg-red-950/20 border border-red-500/30 p-5 rounded-lg flex items-center gap-4">
                 <div className="w-8 h-8 rounded bg-red-600 flex items-center justify-center flex-shrink-0">
                    <Cpu size={18} className="text-white animate-pulse" />
                 </div>
                 <div>
                    <p className="text-[9px] font-black text-red-500 uppercase tracking-widest">Inference Engine</p>
                    {/* THIS IS THE DYNAMIC HARDWARE TEXT */}
                    <p className="text-[10px] text-white font-bold uppercase leading-tight mt-1">
                      {report.forensics.hardware}
                    </p>
                 </div>
              </div>
            </div>

          </div>
        )}
      </main>
    </div>
  );
};

export default App;