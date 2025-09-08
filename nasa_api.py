import requests
import os
from dotenv import load_dotenv

load_dotenv()

NASA_KEY = os.environ.get('NASA_KEY')
print("NASA_API_KEY =", NASA_KEY)
NASA_APOD_URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}"


def get_apod_data():
    response = requests.get(NASA_APOD_URL)
    print(response.json())
    data = response.json()

    return data
