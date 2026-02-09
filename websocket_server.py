"""
websocket_server.py
Ce script lance un serveur WebSocket avec Sanic pour la diffusion en temps réel.
Il permet à Flask de déclencher des notifications via HTTP et gère les connexions WebSocket clients.
"""

# Configuration du logging pour la journalisation des erreurs et informations
import logging
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application principale Sanic
app = Sanic("websocket_server")
connected = set()

# Endpoint HTTP pour diffusion broadcast (déclenché par un appel HTTP depuis Flask)
@app.post("/broadcast")
async def broadcast(request: Request):
    msg = (request.json or {}).get("message", "update")
    for client in list(connected):
        try:
            await client.send(msg)
        except Exception as e:
            logger.error(f"Broadcast send error: {e}")
    return text("Broadcast sent")

# WebSocket - Diffuse les messages à tous les clients, sauf à l'expéditeur (pas d'écho)
@app.websocket('/ws')
async def feed(request, ws):
    connected.add(ws)
    try:
        async for data in ws:
            for client in connected:
                if client is not ws:
                    await client.send(f"Broadcast: {data}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        connected.remove(ws)

# Démarrage du serveur Sanic sur le port 8001
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)