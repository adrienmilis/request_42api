import os
import requests, json
from dotenv import load_dotenv

def main():

    load_dotenv()
    SECRET = os.environ.get('SECRET')
    UID = os.environ.get('UID')
    REDIRECT_URI = "https://httpbin.org/anything"
    url = 'https://api.intra.42.fr'
    uri = '/oauth/token'
    params = {
        'grant_type': 'client_credentials',
        'client_id': UID,
        'client_secret': SECRET
    }

    data = requests.post(f'{url}{uri}', data=params)
    if (data.status_code != 200):
        print("Couldn't get access token. Exiting.")
        exit(1)
    access_token = json.loads(data.text)['access_token']


if __name__ == '__main__':
    main()