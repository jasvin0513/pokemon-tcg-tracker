import os
import requests
from dotenv import load_dotenv

# Load my API key
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure to set it in the .env file.")

print(api_key)