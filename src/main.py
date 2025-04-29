import os
import webbrowser
from hashlib import md5
import requests
from dotenv import load_dotenv, find_dotenv

def get_api_sig(params: dict, secret: str):
    sorted_params = sorted(params.items())
    unhashed_sig = ""
    for key, value in sorted_params:
        unhashed_sig += f"{key}{value}"
    unhashed_sig += secret
    sig = md5(unhashed_sig.encode()).hexdigest()
    return sig

def get_token(api_key):
    response = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key={api_key}&format=json')
    return response.json()['token']

def get_session(api_key, token, secret):
    response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=auth.getSession&api_key={api_key}&token={token}&api_sig={\
        get_api_sig({'api_key': api_key, 'token': token, 'method': 'auth.getSession'}, secret)\
    }&format=json")
    return response.json()

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

api_key = os.getenv("API_KEY")
secret = os.getenv("SECRET")
print(f"API key is {api_key}")
print(f"Secret is {secret}")

session_token = os.getenv("SESSION_TOKEN")
if session_token is None:
    token = get_token(api_key)
    print(f"Token is {token}")

    webbrowser.open(f"http://www.last.fm/api/auth/?api_key={api_key}&token={token}")
    input("Press Enter after authorizing the app on last.fm...") # way too lazy to do this in a better way

    session_token = get_session(api_key, token, secret)["session"]["key"]
    with open(dotenv_path, 'a') as f:
        f.write(f"SESSION_TOKEN = {session_token}\n")

print(f"Session token is {session_token}")
