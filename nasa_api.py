import requests
import os


NASA_KEY = os.environ.get('NASA_KEY')
NASA_APOD_URL = f"https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}"


def get_apod_data():
    response = requests.get(NASA_APOD_URL)
    data = response.json()

    return data
