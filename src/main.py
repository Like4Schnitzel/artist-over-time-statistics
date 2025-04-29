from dotenv import load_dotenv, find_dotenv
import requests
import os

def get_token(api_key):
    response = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key={api_key}&format=json')
    return response.json()['token']

"""
TODO
* If you really don't trust your users, is it worth trying to ping a basic request off the api to make sure the key isn't mistyped
* or has trailing whitespace or something weird before saving it to somewhere you dont' expect them to find?
"""
if find_dotenv() == "":
    with open('.env', 'w') as f:
        api_key = input("Enter your last.fm API key: ")
        f.write(f"API_KEY = {api_key}\n")
load_dotenv()

api_key = os.getenv("API_KEY")
print(f"API key is {api_key}")

token = get_token(api_key)
print(f"Token is {token}")
