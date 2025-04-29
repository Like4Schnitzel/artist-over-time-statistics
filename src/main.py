from dotenv import load_dotenv, find_dotenv
import os

if find_dotenv() == "":
    with open('.env', 'w') as f:
        api_key = input("Enter your last.fm API key: ")
        f.write(f"API_KEY = {api_key}\n")
load_dotenv()

api_key = os.getenv("API_KEY")
print(f"API key is {api_key}")
