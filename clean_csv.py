import pandas as pd
import glob

# 1. On cherche tous les fichiers qui commencent par 'F1' dans ton dossier
fichiers_csv = glob.glob("F1*.csv")
print(f"📂 {len(fichiers_csv)} fichiers trouvés : {fichiers_csv}")

# 2. On définit UNIQUEMENT les colonnes que tu as déjà dans Supabase
# Cela évite l'erreur 'Data Incompatible'
colonnes_compatibles = ['Div', 'Date', 'Time', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']

liste_df = []

for f in fichiers_csv:
    try:
        # On lit le fichier
        df = pd.read_csv(f)
        # On ne garde que les colonnes qui existent dans ta table
        df_clean = df[colonnes_compatibles]
        liste_df.append(df_clean)
        print(f"✅ {f} nettoyé")
    except Exception as e:
        print(f"❌ Erreur sur {f}: {e}")

# 3. On fusionne tout en un seul 'Mega Fichier'
if liste_df:
    mega_base = pd.concat(liste_df, ignore_index=True)
    mega_base.to_csv("mega_historique_pret.csv", index=False)
    print(f"\n🏆 TERMINÉ : Ton fichier 'mega_historique_pret.csv' est prêt !")
    print(f"📊 Total de matchs à importer : {len(mega_base)}")