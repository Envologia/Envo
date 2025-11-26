# Envo Userbot - Session Generator
# Created by @envologia

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("Envo Userbot Session Generator")
print("---------------------------------")
print("This script will help you generate a Telethon session string for your userbot.")
print("You will be asked for your API Key, API Hash, and phone number.")
print("You will also be asked for a login code and your 2FA password if you have one enabled.")
print("\nYour credentials are not stored anywhere. This script is safe to use.")
print("---------------------------------")

API_KEY = input("Enter your API Key: ")
API_HASH = input("Enter your API Hash: ")

with TelegramClient(StringSession(), API_KEY, API_HASH) as client:
    session_string = client.session.save()
    print("\n---------------------------------")
    print("Your session string has been generated successfully!")
    print("Please copy the following string and save it in a safe place.")
    print("You will need this for the SESSION environment variable.")
    print("---------------------------------")
    print(session_string)
    print("---------------------------------")
