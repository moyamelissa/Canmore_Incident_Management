"""
websocket_server.py
Ce script lance un serveur WebSocket avec Sanic pour la diffusion en temps réel.
Il permet à Flask de déclencher des notifications via HTTP et gère les connexions WebSocket clients.
"""


# Importation des modules nécessaires pour Sanic et la gestion WebSocket
from sanic import Sanic
from sanic.response import json, text
from sanic.request import Request


# Création de l'application principale Sanic pour le serveur WebSocket
app = Sanic("websocket_server")


# Endpoint HTTP pour diffusion (déclenché par Flask)
@app.post("/broadcast")
async def broadcast(request: Request):
    msg = (request.json or {}).get("message", "update")
    for client in list(connected):
        try:
            await client.send(msg)
        except Exception:
            pass
    return text("Broadcast sent")


# Stocke les clients WebSocket connectés
connected = set()


# WebSocket - Diffusion en temps réel à tous les clients
@app.websocket('/ws')
async def feed(request, ws):
    connected.add(ws)
    try:
        async for data in ws:
            for client in connected:
                if client is not ws:
                    await client.send(f"Broadcast: {data}")
    except Exception:
        pass
    finally:
        connected.remove(ws)


# Démarrage du serveur Sanic sur le port 8001
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
