import os
import requests
import google.generativeai as genai
from supabase import create_client
from dotenv import load_dotenv

try:
    from duckduckgo_search import DDGS
except ImportError:
    from ddgs import DDGS

# 1. Configuration des services
load_dotenv(dotenv_path=".env.local")

URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") 
GEMINI = os.getenv("GEMINI_API_KEY")
ODDS_API = os.getenv("ODDS_API_KEY")

if not KEY or not URL:
    raise ValueError("❌ Erreur : Les clés Supabase sont manquantes.")

supabase = create_client(URL, KEY)
genai.configure(api_key=GEMINI)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_team_logo(team_name):
    """Recherche le logo transparent du club"""
    try:
        with DDGS() as ddgs:
            search = f"{team_name} football club logo png transparent"
            results = list(ddgs.images(search, max_results=1))
            return results[0]['image'] if results else None
    except: return None

def scruter_le_web(home, away):
    """Récupère les actus via DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(f"lineup injuries {home} vs {away}", max_results=3)]
            return "\n".join(results)
    except: return "Pas de news fraîches."

def expert_ia(home, away, cote, actus):
    """Analyse tactique avec intelligence artificielle"""
    prompt = f"Expert Foot : Analyse {home} vs {away} (Cote: {cote}). Actus: {actus}. Rédige 2 lignes de scouting précises."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except: return "Analyse tactique en cours..."

def lancer_analyse():
    print("🚀 --- Mission Scout IA en cours ---")
    supabase.table("predictions").delete().neq("id", 0).execute() # Nettoyage

    url = f"https://api.the-odds-api.com/v4/sports/soccer_uefa_champs_league/odds/?apiKey={ODDS_API}&regions=eu&markets=h2h"
    matchs = requests.get(url).json()

    for m in matchs:
        home, away = m['home_team'], m['away_team']
        try:
            outcomes = m['bookmakers'][0]['markets'][0]['outcomes']
            c_h = next(o['price'] for o in outcomes if o['name'] == home)
            
            print(f"🕵️‍♂️ Analyse de {home}...")
            h_logo = get_team_logo(home)
            a_logo = get_team_logo(away)
            actus = scruter_le_web(home, away)
            analyse = expert_ia(home, away, c_h, actus)

            # Publication vers Supabase avec les bons noms de colonnes
            supabase.table("predictions").insert({
                "home_team": home,
                "away_team": away,
                "home_logo": h_logo,
                "away_logo": a_logo,
                "prediction": analyse,
                "odds": c_h,
                "probability": int((1/c_h)*100),
                "is_value": c_h > 2.2,
                "sport": "⚽ Champions League"
            }).execute()
            print(f"✅ {home} publié.")
        except Exception as e: continue

    print("🏁 Fin de mission.")

if __name__ == "__main__":
    lancer_analyse()