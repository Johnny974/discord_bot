import requests


def get_dad_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["joke"]
    else:
        return "Prepáč, API call na získanie vtipu nefungoval."
