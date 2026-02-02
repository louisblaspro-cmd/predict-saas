"use client";
import { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function Home() {
  const [predictions, setPredictions] = useState<any[]>([]);

  useEffect(() => {
    const fetchMatches = async () => {
      const { data } = await supabase.from('predictions').select('*').order('created_at', { ascending: false });
      if (data) setPredictions(data);
    };
    fetchMatches();
  }, []);

  return (
    <main className="min-h-screen bg-[#020617] text-white p-8">
      <h1 className="text-5xl font-black mb-12 italic text-blue-500 text-center tracking-tighter">Scout Intelligence 2.0 🚀</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {predictions.map((p) => (
          <div key={p.id} className="bg-[#0f172a] border border-slate-800 rounded-[2.5rem] p-7 shadow-2xl transition-all hover:border-blue-500/30">
            {/* Logos & Equipes */}
            <div className="flex justify-between items-center mb-8">
              <div className="flex flex-col items-center w-2/5 text-center">
                <img src={p.home_logo || "/placeholder.png"} className="w-16 h-16 object-contain mb-3 drop-shadow-xl" alt="L" />
                <span className="text-[10px] font-bold uppercase tracking-widest">{p.home_team}</span>
              </div>
              <div className="text-xl font-black italic text-slate-600">VS</div>
              <div className="flex flex-col items-center w-2/5 text-center">
                <img src={p.away_logo || "/placeholder.png"} className="w-16 h-16 object-contain mb-3 drop-shadow-xl" alt="R" />
                <span className="text-[10px] font-bold uppercase tracking-widest">{p.away_team}</span>
              </div>
            </div>

            {/* Analyse IA */}
            <div className="mb-8 p-4 bg-slate-900/50 rounded-2xl border border-slate-800">
              <p className="text-slate-300 text-xs italic leading-relaxed">"{p.prediction}"</p>
            </div>

            {/* Stats */}
            <div className="flex justify-between pt-6 border-t border-slate-800/50">
              <div>
                <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">Confiance</p>
                <p className="text-3xl font-black text-blue-500">{p.probability}%</p>
              </div>
              <div className="text-right">
                <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">Cote Live</p>
                <p className="text-2xl font-black text-white bg-slate-800 px-3 py-1 rounded-lg italic">{p.odds}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}