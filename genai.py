import os

from google import genai
from google.genai import types
from google.genai.errors import APIError

from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key = API_KEY)
SYSTEM_BOT = client.chats.create(model="gemini-3.5-flash",
                           config=types.GenerateContentConfig(system_instruction= SYSTEM_PROMPT))
def bot(msg):
    try:
        response = SYSTEM_BOT.send_message(msg)
        return response.text
    except APIError as e:
        return e.code

# For testing
if __name__ == "__main__":
    response = bot("google")
    print(type(response))
    print(response)
    