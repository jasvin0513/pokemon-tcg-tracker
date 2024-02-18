import json

# Your JSON data
json_data = '''
{
  "data": [
    {
      "id": "g1-1",
      "name": "Venusaur-EX",
      "types": [
        "Grass"
      ],
      "evolvesTo": [
        "M Venusaur-EX"
      ],
      "attacks": [
        {
          "name": "Frog Hop",
          "cost": [
            "Grass",
            "Colorless",
            "Colorless"
          ],
          "convertedEnergyCost": 3,
          "damage": "40+",
          "text": "Flip a coin. If heads, this attack does 40 more damage."
        }
      ],
      "weaknesses": [
        {
          "type": "Fire",
          "value": "×2"
        }
      ],
      "retreatCost": [
        "Colorless",
        "Colorless",
        "Colorless",
        "Colorless"
      ],
      "rarity": "Rare Holo EX",
      "nationalPokedexNumbers": [
        3
      ]
    },
    {
      "id": "g1-1",
      "name": "Venusaur-EX",
      "types": [
        "Grass"
      ],
      "evolvesTo": [
        "M Venusaur-EX"
      ],
      "attacks": [
        {
          "name": "Frog Hop",
          "cost": [
            "Grass",
            "Colorless",
            "Colorless"
          ],
          "convertedEnergyCost": 3,
          "damage": "40+",
          "text": "Flip a coin. If heads, this attack does 40 more damage."
        }
      ],
      "weaknesses": [
        {
          "type": "Fire",
          "value": "×2"
        }
      ],
      "retreatCost": [
        "Colorless",
        "Colorless",
        "Colorless",
        "Colorless"
      ],
      "rarity": "Rare Holo EX",
      "nationalPokedexNumbers": [
        3
      ]
    },
    {
      "id": "g1-1",
      "name": "Venusaur-EX",
      "types": [
        "Grass"
      ],
      "evolvesTo": [
        "M Venusaur-EX"
      ],
      "attacks": [
        {
          "name": "Frog Hop",
          "cost": [
            "Grass",
            "Colorless",
            "Colorless"
          ],
          "convertedEnergyCost": 3,
          "damage": "40+",
          "text": "Flip a coin. If heads, this attack does 40 more damage."
        }
      ],
      "weaknesses": [
        {
          "type": "Fire",
          "value": "×2"
        }
      ],
      "retreatCost": [
        "Colorless",
        "Colorless",
        "Colorless",
        "Colorless"
      ],
      "rarity": "Rare Holo EX",
      "nationalPokedexNumbers": [
        3
      ]
    }
  ],
  "page": 1,
  "pageSize": 250,
  "count": 117,
  "totalCount": 117
}
'''

# Parse the JSON data
parsed_data = json.loads(json_data)

# Extract each card
cards = parsed_data.get("data", [])

for card in cards:
  print(json.dumps(card.get("name"), indent = 2))
  print("-" * 50)
