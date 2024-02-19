import os
import json
import requests
from dotenv import load_dotenv

# Load my API key
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure to set it in the .env file.")


# Search cards
def search_cards(user_params = None):
    # Load API
    url = "https://api.pokemontcg.io/v2/cards"
    headers = {"X-Api-Key": api_key}
    params = {'q' : user_params}

    # Set parameters and send a request
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
        
# Get sets
def get_sets():
    # Load API
    url = "https://api.pokemontcg.io/v2/sets"
    headers = {"X-Api-Key": api_key}
    params = {'orderBy' : 'releaseDate'}

    # Set parameters and send a request
    response = requests.get(url, headers = headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        
    sets = data.get("data", [])
    set_data = {}
    
    # Get the symbol of each set
    for set in sets:
        set_data[set.get("name")] = set.get("images").get("symbol")
        
    return set_data

search_cards('id:xy1')