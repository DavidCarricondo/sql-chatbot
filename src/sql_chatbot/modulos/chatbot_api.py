import requests
from dotenv import load_dotenv
import os
load_dotenv()

def api_call():
    """
    Makes an API call to NASA's Astronomy Picture of the Day (APOD) endpoint.

    This function retrieves the title, explanation, and image URL of the APOD
    using the NASA API key stored in the environment variable 'API_KEY_NASA'.

    Returns:
        dict: A dictionary containing the following keys:
            - 'title' (str): The title of the APOD. Defaults to "No title available" if not present.
            - 'explanation' (str): The explanation of the APOD. Defaults to "No explanation available" if not present.
            - 'image_url' (str): The URL of the APOD image. Defaults to an empty string if not present.
    """
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


