# app/openai_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o",  # O el modelo que prefieras
        messages=messages
    )
    return response.choices[0].message.content
