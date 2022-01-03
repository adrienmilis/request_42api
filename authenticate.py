import requests, os, json
from dotenv import load_dotenv
from urllib.parse import urlencode
import webbrowser
import sqlite3
from contextlib import closing
from datetime import datetime

TOKEN_EXPIRY = 7200

load_dotenv()
SECRET = os.environ.get('SECRET')
UID = os.environ.get('UID')
REDIRECT_URI = 'https://projects.intra.42.fr'

def get_code(url):

    params = {
        'client_id': UID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'projects public'
    }
    request_url = url + '?' + urlencode(params)
    webbrowser.open(request_url)
    return (input("Enter the code (present in the URL): "))

def get_access_token(code):

    url = 'https://api.intra.42.fr/oauth/token'
    params = {
        'grant_type': 'authorization_code',
        'client_id': UID,
        'client_secret': SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    data = requests.post(url, data=params)
    if (data.status_code != 200):
        print('Error while retrieving access token')
        exit(1)
    access_token = json.loads(data.text)['access_token']
    return (access_token)

def token_is_still_valid(token_date):
    # turn token_date it into datetime object
    token_date_object = datetime.strptime(token_date, '%Y-%m-%d %H:%M:%S')
    # get diff with datetime.now()
    diff = datetime.now() - token_date_object
    if (diff.seconds > TOKEN_EXPIRY):
        return False
    return True


def check_valid_token(username):
    
    with closing(sqlite3.connect('api_tokens.db')) as con:
        with closing(con.cursor()) as cur:
        
            cur.execute('''CREATE TABLE IF NOT EXISTS tokens
                            (date text, username text, token text)''')
            for row in cur.execute("SELECT * from tokens"):
                if (row[1] == username):
                    # check date is less than 2 hours
                    if (token_is_still_valid(row[0])):
                        return (row[2])
            return (None)

def add_token_to_db(username, token):

    with closing(sqlite3.connect('api_tokens.db')) as con:
        with closing(con.cursor()) as cur:
            cur.execute(f"""INSERT INTO tokens VALUES (
                '{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}',
                '{username}',
                '{token}'
                )""")
            con.commit()
            print('Token successfully added to database')

def main():

    url = 'https://api.intra.42.fr/oauth/authorize'
    username = input("Enter 42 intra username: ")

    # here we check the database for a valid token
    access_token = check_valid_token(username)
    if (access_token != None):
        print(f"Found access token for user {username}")
    else:
        print('First time user. You will be redirected to authenticate.')
        ans = input('You will need to copy the code in the url after being redirected. Proceed ? (y/n) ')
        if (ans != 'y' and ans != 'Y'):
            exit(0)

        # authenticate user
        code = get_code(url)

        # exchange the code for an access token
        # tokens expire after 2 hours
        access_token = get_access_token(code)
        add_token_to_db(username, access_token)

    # we can now request the api with our access_token
    header = {'Authorization': f'Bearer {access_token}'}

    # test with /v2/achievements
    url = 'https://api.intra.42.fr'
    while (1):
        uri = input("\nEnter the uri to request: ")
        data = requests.get(f'{url}{uri}', headers=header)
        for elem in json.loads(data.text):
            print(elem)

if __name__ == '__main__':
    main()