import os
import webbrowser
from hashlib import md5
import requests
from dotenv import load_dotenv, find_dotenv

def make_api_sig(params: dict, secret: str):
    sorted_params = sorted(params.items())
    unhashed_sig = ""
    for key, value in sorted_params:
        unhashed_sig += f"{key}{value}"
    unhashed_sig += secret
    sig = md5(unhashed_sig.encode()).hexdigest()
    return sig

def fetch_token(api_key):
    response = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key={api_key}&format=json')
    return response.json()['token']

def fetch_session(api_key, token, secret):
    response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=auth.getSession&api_key={api_key}&token={token}&api_sig={\
        make_api_sig({'api_key': api_key, 'token': token, 'method': 'auth.getSession'}, secret)\
    }&format=json")
    return response.json()

def init_auth():
    """
    Gets the API key and returns it.
    """

    """
    TODO
    * If you really don't trust your users, is it worth trying to ping a basic request off the api to make sure the key isn't mistyped
    * or has trailing whitespace or something weird before saving it to somewhere you dont' expect them to find?
    """
    if find_dotenv() == "":
        with open('.env', 'w') as f:
            api_key = input("Enter your last.fm API key: ")
            secret = input("Enter your last.fm Shared secret: ")
            f.write(f"API_KEY = {api_key}\nSECRET = {secret}\n")
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    api_key: str = os.getenv("API_KEY")
    
    return api_key
