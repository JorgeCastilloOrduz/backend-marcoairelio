# app/main.py
from fastapi import FastAPI, HTTPException
from app.schemas import Message
from app.memory import Memory
from app.openai_client import get_response

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory = Memory()

@app.post("/chat/")
async def chat(message: Message):
    try:
        # Agrega el mensaje del usuario al historial
        memory.add_message(message.user_id, "user", message.content)

        # Obtiene el historial de mensajes
        history = memory.get_history(message.user_id)

        # Obtiene la respuesta de OpenAI
        reply = get_response(history)

        # Agrega la respuesta al historial
        memory.add_message(message.user_id, "assistant", reply)

        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
