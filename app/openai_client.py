# app/openai_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_response(messages):

    # Inserta un mensaje de sistema al inicio del historial
    system_message = {
        "role": "system",
        "content": (
            "Eres Marco Aurelio, el emperador romano y filósofo estoico. "
            "Respondes con sabiduría, calma y profundidad. "
            "Tus respuestas deben ser serenas, reflexivas y centradas en el control de las emociones, "
            "siempre con un tono accesible y humano."
        )
    }

    full_messages = [system_message] + messages
    
    response = client.chat.completions.create(
        model="gpt-4o",  # O el modelo que prefieras
        messages=full_messages
    )
    return response.choices[0].message.content
