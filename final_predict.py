import os
import requests
import google.generativeai as genai
from supabase import create_client
from dotenv import load_dotenv

# Correction de l'import (Règle l'erreur de ta capture 23.35.28)
try:
    from duckduckgo_search import DDGS
except ImportError:
    from ddgs import DDGS

# 1. Chargement
print("🔌 Démarrage des services...")
load_dotenv(dotenv_path=".env.local")

# 2. Connexion sécurisée
supabase = create_client(os.getenv("NEXT_PUBLIC_SUPABASE_URL"), os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def scruter_le_web(home, away):
    """Recherche web manuelle pour éviter le bug 404 de Google"""
    print(f"🌐 Scouting web : {home} vs {away}...")
    try:
        with DDGS() as ddgs:
            # On cherche les infos réelles sur le web
            results = [r['body'] for r in ddgs.text(f"football lineup injuries {home} vs {away}", max_results=3)]
            return "\n".join(results)
    except:
        return "Pas de news fraîches."

def expert_ia(home, away, cote, actus):
    """L'IA apprend et analyse via intelligence_scout"""
    # On regarde ce qu'on sait déjà (Apprentissage)
    try:
        memoire = supabase.table("intelligence_scout").select("*").or_(f"sujet.ilike.%{home}%,sujet.ilike.%{away}%").execute()
        souvenirs = "\n".join([m['info_cle'] for m in memoire.data])
    except: souvenirs = ""

    prompt = f"Scout IA : Analyse {home} vs {away} (Cote: {cote}). Actus: {actus}. Mémoire: {souvenirs}. Rédige 2 lignes de scouting."
    try:
        response = model.generate_content(prompt)
        expertise = response.text.strip()
        # On sauvegarde le savoir acquis
        supabase.table("intelligence_scout").insert({"sujet": home, "info_cle": expertise[:100]}).execute()
        return expertise
    except: return "Analyse tactique en cours."

def lancer_analyse():
    print("🚀 --- Lancement de la mission ---")
    supabase.table("predictions").delete().neq("id", 0).execute() # Nettoyage dashboard

    url = f"https://api.the-odds-api.com/v4/sports/soccer_uefa_champs_league/odds/?apiKey={os.getenv('ODDS_API_KEY')}&regions=eu&markets=h2h"
    matchs = requests.get(url).json()

    for m in matchs:
        home, away = m['home_team'], m['away_team']
        try:
            outcomes = m['bookmakers'][0]['markets'][0]['outcomes']
            c_h = next(o['price'] for o in outcomes if o['name'] == home)
            
            print(f"🕵️‍♂️ Traitement : {home}...")
            actus = scruter_le_web(home, away)
            analyse = expert_ia(home, away, c_h, actus)

            # Publication vers Supabase (Syntaxe corrigée de ta capture 23.36.10)
            supabase.table("predictions").insert({
                "match": f"{home} vs {away}",
                "sport": "⚽ Champions League",
                "prono": f"Victoire {home}",
                "cote": c_h,
                "confiance": int((1/c_h)*100),
                "analyse": analyse, 
                "is_value": c_h > 2.2
            }).execute()
            print(f"✅ Match publié.")
        except: continue
    print("🏁 Mission terminée.")

if __name__ == "__main__":
    lancer_analyse()