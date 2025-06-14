import requests
import os
from dotenv import load_dotenv
load_dotenv()

CANVAS_BASE_URL = "https://prepanet.instructure.com/api/v1"
CANVAS_ACCESS_TOKEN = os.getenv("CANVAS_ACCESS_TOKEN")

def get_canvas_headers():
    return {
        "Authorization": f"Bearer {CANVAS_ACCESS_TOKEN}"
    }

def make_canvas_request(endpoint, params=None):
    url = f"{CANVAS_BASE_URL}{endpoint}"
    response = requests.get(url, headers=get_canvas_headers(), params=params)
    
    if response.status_code != 200:
        return None
    
    return response.json()