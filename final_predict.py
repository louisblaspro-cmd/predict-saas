import os
import requests
import google.generativeai as genai
from supabase import create_client
from dotenv import load_dotenv

# Import DuckDuckGo avec gestion d'erreur
try:
    from duckduckgo_search import DDGS
except ImportError:
    from ddgs import DDGS

# 1. Configuration & Connexion
load_dotenv(dotenv_path=".env.local")
supabase = create_client(os.getenv("NEXT_PUBLIC_SUPABASE_URL"), os.getenv("SUPABASE_KEY")) # Utilise la clé Secrète
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_team_logo(team_name):
    """NOUVEAU : Trouve le logo officiel du club"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(f"{team_name} football club logo png transparent", max_results=1))
            return results[0]['image'] if results else None
    except:
        return None

def scruter_le_web(home, away):
    """Ta fonction de recherche de news"""
    print(f"🌐 Scouting web : {home} vs {away}...")
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(f"football lineup injuries {home} vs {away}", max_results=3)]
            return "\n".join(results)
    except:
        return "Pas de news fraîches."

def expert_ia(home, away, cote, actus):
    """Ton IA avec mémoire (Apprentissage)"""
    try:
        memoire = supabase.table("intelligence_scout").select("*").or_(f"sujet.ilike.%{home}%,sujet.ilike.%{away}%").execute()
        souvenirs = "\n".join([m['info_cle'] for m in memoire.data])
    except: souvenirs = ""

    prompt = f"Scout IA : Analyse {home} vs {away} (Cote: {cote}). Actus: {actus}. Mémoire: {souvenirs}. Rédige 2 lignes de scouting."
    try:
        response = model.generate_content(prompt)
        expertise = response.text.strip()
        supabase.table("intelligence_scout").insert({"sujet": home, "info_cle": expertise[:100]}).execute()
        return expertise
    except: return "Analyse tactique en cours."

def lancer_analyse():
    print("🚀 --- Lancement de la mission (Version Logos) ---")
    supabase.table("predictions").delete().neq("id", 0).execute() # Nettoyage

    # Récupération des vrais matchs via ton API
    url = f"https://api.the-odds-api.com/v4/sports/soccer_uefa_champs_league/odds/?apiKey={os.getenv('ODDS_API_KEY')}&regions=eu&markets=h2h"
    matchs = requests.get(url).json()

    for m in matchs:
        home, away = m['home_team'], m['away_team']
        try:
            outcomes = m['bookmakers'][0]['markets'][0]['outcomes']
            c_h = next(o['price'] for o in outcomes if o['name'] == home)
            
            print(f"🕵️‍♂️ Traitement : {home} vs {away}...")
            
            # Action ! Récupération logos + news + analyse
            h_logo = get_team_logo(home)
            a_logo = get_team_logo(away)
            actus = scruter_le_web(home, away)
            analyse = expert_ia(home, away, c_h, actus)

            # Publication enrichie vers Supabase
            supabase.table("predictions").insert({
                "home_team": home,
                "away_team": away,
                "home_logo": h_logo,
                "away_logo": a_logo,
                "prediction": analyse, # Renommé pour correspondre au frontend
                "odds": c_h,           # Renommé pour correspondre au frontend
                "probability": int((1/c_h)*100),
                "is_value": c_h > 2.2,
                "sport": "⚽ Champions League"
            }).execute()
            print(f"✅ Match publié avec logos.")
        except Exception as e: 
            print(f"❌ Erreur sur un match : {e}")
            continue
            
    print("🏁 Mission terminée.")

if __name__ == "__main__":
    lancer_analyse()