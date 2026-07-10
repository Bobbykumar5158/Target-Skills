import os

from google import genai
from google.genai import types
from google.genai.errors import APIError

from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

import json

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key = API_KEY)
SYSTEM_BOT = client.chats.create(model="gemini-3.5-flash",
                           config=types.GenerateContentConfig(
                               system_instruction= SYSTEM_PROMPT,
                               response_mime_type="application/json"
                               )
                            )

def bot(msg, max_retries=3):
    current_msg = msg
    
    for attempt in range(max_retries):
        try:
            response = SYSTEM_BOT.send_message(current_msg)
            
            try:
                data = json.loads(response.text)
                return json.dumps({
                    "status_code" : 200,
                    "response" : data
                })
                
            except json.JSONDecodeError:
                current_msg = (
                    "Your last response was not valid JSON and failed to parse. "
                    "Please rewrite your previous response. Output ONLY valid JSON matching the requested schema. "
                    "Do not include conversational text or markdown ticks outside the JSON structure."
                )
                
        except APIError as e:
            return json.dumps({
                "status_code": e.code,
                "response": e.message,
            })
            
    return json.dumps({
        "status_code" : 502,
        "response" : "Max tries reached"
    })

# For testing
if __name__ == "__main__":
    msg = input("Enter here :")
    response = bot(msg)
    print(type(response))
    print(response)
    