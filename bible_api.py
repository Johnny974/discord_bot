import requests


def get_random_bible_verse():
    url = 'https://bible-api.com/data/web/random'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        verse = data['random_verse']['text']
        coordinates = f'{data['random_verse']['book']} {data["random_verse"]['chapter']}, {data["random_verse"]['verse']}'
        formatted_verse = f'Random bible verse: {verse}({coordinates})'
        return formatted_verse


print(get_random_bible_verse())
