import requests
import os
from supabase import create_client

# Utilise tes clés Supabase
url = "https://aztetkevujaoturgeyqb.supabase.co"
key = "votre_cle_anon" # Prends celle de ton fichier .env
supabase = create_client(url, key)

def update_real_matches():
    api_key = "37bf6064964d74e3e154c09ce977e737" # Ta clé Odds API
    # On récupère la Ligue 1 (soccer_france_ligue_1)
    api_url = f"https://api.the-odds-api.com/v4/sports/soccer_france_ligue_1/odds/?apiKey={api_key}&regions=eu&markets=h2h"
    
    response = requests.get(api_url)
    matches = response.json()

    for m in matches:
        # On extrait les infos réelles
        match_name = f"{m['home_team']} vs {m['away_team']}"
        # On prend la première cote disponible (ex: Unibet ou Winamax)
        cote_home = m['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
        
        # On envoie à Supabase
        supabase.table("predictions").insert({
            "match": match_name,
            "sport": "⚽ Football",
            "cote": cote_home,
            "prono": f"Victoire {m['home_team']}",
            "confiance": 0, # On va calculer ça à l'étape 3 !
        }).execute()
        print(f"✅ Match ajouté : {match_name}")

update_real_matches()