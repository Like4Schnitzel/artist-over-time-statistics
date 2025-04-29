from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv()
if dotenv_path == "":
    with open('.env', 'w') as f:
        token = input("Enter your last.fm API key: ")
        f.write(f"TOKEN = {token}\n")
load_dotenv(dotenv_path)

token = os.getenv("TOKEN")
print(f"Token is {token}")
