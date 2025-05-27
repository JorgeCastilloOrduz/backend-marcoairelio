#!/usr/bin/env python

import asyncio
import websockets
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Inicializa el cliente de OpenAI con la clave desde variable de entorno
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Función que interactúa con la API de OpenAI
async def get_openai_response(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # o "gpt-4o-mini" si prefieres
            messages=[
                {"role": "system", "content": "Eres el filósofo Marco Aurelio. Responde con sabiduría, calma y profundidad, pero de forma comprensible para cualquiera."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error al llamar a OpenAI: {e}", flush=True)
        return "Lo siento, hubo un error al procesar tu mensaje."

# Manejador del websocket
async def handle_connection(websocket):
    try:
        async for message in websocket:
            print("Mensaje recibido:", message, flush=True)

            response = await get_openai_response(message)

            await websocket.send(response)
            await websocket.send("[END]")
    except websockets.exceptions.ConnectionClosed:
        print("Cliente desconectado", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)

# Servidor principal
async def main():
    print("Iniciando servidor WebSocket...", flush=True)

    async with websockets.serve(
        handle_connection,
        "0.0.0.0",
        int(os.environ.get('PORT', 8090))
    ):
        print("Servidor WebSocket corriendo en el puerto 8090", flush=True)
        await asyncio.Future()  # Mantiene el servidor corriendo

if __name__ == "__main__":
    asyncio.run(main())
