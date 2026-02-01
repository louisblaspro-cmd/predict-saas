import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default async function Home() {
  // Correction syntaxe .from()
  const { data: predictions } = await supabase
    .from('predictions') 
    .select('*')
    .order('created_at', { ascending: false });

  return (
    <main className="min-h-screen bg-[#020617] text-white p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-5xl font-black mb-12 italic text-blue-500 tracking-tighter">Scout Intelligence 2.0 🚀</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {predictions?.map((p) => (
            <div key={p.id} className="bg-[#0f172a] border border-slate-800 rounded-[2.5rem] p-7 shadow-2xl transition-all hover:border-blue-500/30 group">
              <h2 className="text-2xl font-extrabold mb-4 group-hover:text-blue-400 transition-colors">{p.match}</h2>
              <div className="mb-8 p-4 bg-slate-900 rounded-2xl border border-slate-800">
                <p className="text-slate-300 text-xs italic leading-relaxed">"{p.analyse}"</p>
              </div>
              <div className="flex justify-between border-t border-slate-800/50 pt-6">
                <div><p className="text-3xl font-black text-blue-500">{p.confiance}%</p></div>
                <div className="text-right"><p className="text-3xl font-black text-white">{p.cote}</p></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}