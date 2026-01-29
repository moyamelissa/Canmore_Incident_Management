
# =========================
# Titre: Importations
# Explication: Importation des modules nécessaires pour Sanic et la gestion WebSocket
from sanic import Sanic
from sanic.response import json, text
from sanic.request import Request

# =========================
# Titre: Initialisation de l'application Sanic
# Explication: Création de l'application principale Sanic pour le serveur WebSocket
app = Sanic("websocket_server")


# =========================
# Titre: Endpoint HTTP pour diffusion
# Explication: Permet à Flask de déclencher une diffusion WebSocket via une requête POST
@app.post("/broadcast")
async def broadcast(request: Request):
    msg = (request.json or {}).get("message", "update")
    # Diffuse à tous les clients WebSocket connectés
    for client in list(connected):
        try:
            await client.send(msg)
        except Exception:
            pass
    return text("Broadcast sent")


# =========================
# Titre: Gestion des connexions WebSocket
# Explication: Stocke les clients WebSocket connectés
connected = set()



# =========================
# Titre: WebSocket - Diffusion en temps réel
# Explication: Gère les connexions WebSocket et la diffusion des messages à tous les clients
@app.websocket('/ws')
async def feed(request, ws):
    connected.add(ws)
    try:
        async for data in ws:
            # Diffuse à tous les clients connectés sauf l'expéditeur
            for client in connected:
                if client is not ws:
                    await client.send(f"Broadcast: {data}")
    except Exception:
        pass
    finally:
        connected.remove(ws)



# =========================
# Titre: Lancement du serveur WebSocket
# Explication: Démarre le serveur Sanic sur le port 8001
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
