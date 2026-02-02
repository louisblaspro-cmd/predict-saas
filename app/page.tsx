// ... (haut du fichier inchangé)
{predictions?.map((p) => (
  <div key={p.id} className="bg-[#0f172a] border border-slate-800 rounded-[2.5rem] p-7 shadow-2xl transition-all hover:border-blue-500/30">
    {/* Logos & Equipes */}
    <div className="flex justify-between items-center mb-8">
      <div className="flex flex-col items-center w-2/5 text-center">
        <img src={p.home_logo || "/placeholder.png"} className="w-16 h-16 object-contain mb-3" alt="L" />
        <span className="text-[10px] font-bold uppercase">{p.home_team || "Équipe"}</span>
      </div>
      <div className="text-xl font-black italic text-slate-600">VS</div>
      <div className="flex flex-col items-center w-2/5 text-center">
        <img src={p.away_logo || "/placeholder.png"} className="w-16 h-16 object-contain mb-3" alt="R" />
        <span className="text-[10px] font-bold uppercase">{p.away_team || "Équipe"}</span>
      </div>
    </div>

    {/* Analyse IA */}
    <div className="mb-8 p-4 bg-slate-900/50 rounded-2xl border border-slate-800">
      <p className="text-slate-300 text-xs italic leading-relaxed">
        "{p.prediction || "Analyse en cours..."}"
      </p>
    </div>

    {/* Stats - Les || 0 évitent le crash si la colonne est vide */}
    <div className="flex justify-between pt-6 border-t border-slate-800/50">
      <div>
        <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">Confiance</p>
        <p className="text-3xl font-black text-blue-500">{p.probability || 0}%</p>
      </div>
      <div className="text-right">
        <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">Cote</p>
        <p className="text-2xl font-black text-white bg-slate-800 px-3 py-1 rounded-lg italic">{p.odds || "1.00"}</p>
      </div>
    </div>
  </div>
))}