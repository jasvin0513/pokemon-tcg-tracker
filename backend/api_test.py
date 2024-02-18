import os
import json
import requests
from dotenv import load_dotenv

# Load my API key
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure to set it in the .env file.")

# Load API
url = "https://api.pokemontcg.io/v2/cards"
headers = {"X-Api-Key": api_key}
params = {'q': 'name:charizard'}
response = requests.get(url, headers = headers, params=params)

if response.status_code == 200:
    data = response.json()
else:
    print("Failed to retrieve data. Status code:", response.status_code)

# Extract each card from the data
cards = data.get("data", [])

for card in cards:
  print(json.dumps(card.get("name"), indent = 2))
  print("-" * 50)
