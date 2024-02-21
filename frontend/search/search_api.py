"""
This script searches the Pokemon TCG API and converts the JSON files into a card object
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load my API key
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure to set it in the .env file.")

class Card():
    def __init__(self, data):
        self.supertype = data.get("supertype")
        self.name = data.get("name")
        self.nationalPokedexNumbers = data.get("nationalPokedexNumbers")
        self.set = data.get("set", {}).get("name")
        self.setNo = data.get("number")
        self.types = data.get("types", [])
        self.image = data.get("images",{}).get("small")
        
        if data.get("subtypes") and len(data.get("subtypes")) > 1:
            self.subtype = data.get("subtypes", [])[-1]
        else:
            self.subtype = data.get("subtypes")
        
        self.price = self.set_price(data)
        
    def __str__(self):
        return f"Card: {self.name}\nSupertype: {self.supertype}\nSet: {self.set}\nSet Number: {self.setNo}\nTypes: {self.types}\nSubtypes: {self.subtype}\nPrice: {self.price}"
        
    # Price function to avoid having missing prices
    def set_price(self, data):
        if data.get("cardmarket", {}).get("prices", {}).get("averageSellPrice") != None:
            return float(data.get("cardmarket", {}).get("prices", {}).get("averageSellPrice")) * 1.45
        else:
            return float(data.get("tcgplayer", {}).get("prices", {}).get("holofoil", {}).get("market")) * 1.35
    
# Search cards
def search_cards(user_params = None):
    # Load API
    url = "https://api.pokemontcg.io/v2/cards"
    headers = {"X-Api-Key": api_key}
    params = {'q' : user_params}

    # Set parameters and send a request
    response = requests.get(url, headers = headers, params = params)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

    # Extract each card from the data
    card_data = data.get("data", [])
    parsed_cards = []

    for card in card_data:
        parsed_card = Card(card)
        parsed_cards.append(parsed_card)
    
    return parsed_cards
        
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
    
    # Parse the JSON data and store the set data
    sets = data.get("data", [])
    set_data = []
    
    # Get the symbol of each set
    for set in sets:
        set_data.append((set.get("name"), set.get("id"), set.get("images").get("symbol")))
        
    return set_data