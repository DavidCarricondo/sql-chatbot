import requests
from dotenv import load_dotenv
import os
load_dotenv()

def api_call():
    api_key = os.getenv("API_KEY")
    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
    return response.json()

if __name__ == "__main__":
    print(api_call())


