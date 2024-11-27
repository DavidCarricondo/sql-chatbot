import requests
from dotenv import load_dotenv
import os
load_dotenv()

def api_call():
    api_key = os.getenv("API_KEY_NASA")
    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
    data = response.json()
    return {
        "title": data.get("title", "No title available"),
        "explanation": data.get("explanation", "No explanation available"),
        "image_url": data.get("url", ""),
    }

if __name__ == "__main__":
    print(api_call())


