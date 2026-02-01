import requests

API_KEY = "37bf6064964d74e3e154c09ce977e737"
url = f"https://api.the-odds-api.com/v4/sports/?apiKey={API_KEY}"

response = requests.get(url).json()

print("listes des sports disponibles actuellement :")
for sport in response:
    if "soccer" in sport['key']:
        print(f"⚽ {sport['title']} -> Code à utiliser : {sport['key']}")