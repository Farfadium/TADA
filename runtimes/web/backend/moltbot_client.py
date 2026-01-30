"""Client WebSocket pour communiquer avec Moltbot Gateway."""
import asyncio
import json
import uuid
from typing import Optional, Dict, Any, List
import websockets

GATEWAY_URL = "ws://127.0.0.1:18789"
GATEWAY_TOKEN = "ef6c68e50f27b0c0aaa2b91e706480d9a3cde125fec8320149ecc59b6008500f"
SESSION_KEY = "agent:main:main"
PROTOCOL_VERSION = 3


class MoltbotClient:
    def __init__(self):
        self.ws = None
        self.pending_requests: Dict[str, asyncio.Future] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self._listener_task = None
        self.connected = False
    
    async def connect(self):
        """Connecte au Gateway WebSocket."""
        if self.ws and self.connected:
            return
        
        self.ws = await websockets.connect(GATEWAY_URL)
        self._listener_task = asyncio.create_task(self._listen())
        
        # Attendre le challenge
        try:
            challenge = await asyncio.wait_for(self.event_queue.get(), timeout=5)
            if challenge.get("event") == "connect.challenge":
                # Envoyer connect avec auth
                result = await self._send_request("connect", {
                    "minProtocol": PROTOCOL_VERSION,
                    "maxProtocol": PROTOCOL_VERSION,
                    "client": {
                        "id": "gateway-client",
                        "version": "0.2.0",
                        "platform": "linux",
                        "mode": "backend"
                    },
                    "caps": [],
                    "commands": [],
                    "role": "operator",
                    "scopes": ["operator.admin"],
                    "auth": {"token": GATEWAY_TOKEN}
                })
                
                if result.get("ok"):
                    self.connected = True
                else:
                    raise Exception(f"Auth failed: {result.get('error')}")
        except asyncio.TimeoutError:
            raise Exception("Connection timeout")
    
    async def _listen(self):
        """Écoute les messages du Gateway."""
        try:
            async for message in self.ws:
                data = json.loads(message)
                await self._handle_message(data)
        except websockets.exceptions.ConnectionClosed:
            self.connected = False
        except Exception:
            self.connected = False
    
    async def _handle_message(self, data: Dict[str, Any]):
        """Traite un message reçu."""
        # Réponse à une requête
        if "id" in data and data["id"] in self.pending_requests:
            future = self.pending_requests.pop(data["id"])
            if not future.done():
                future.set_result(data)
            return
        
        # Event
        await self.event_queue.put(data)
    
    async def _send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Envoie une requête au Gateway."""
        request_id = str(uuid.uuid4())
        request = {
            "type": "req",
            "id": request_id,
            "method": method,
            "params": params or {}
        }
        
        future = asyncio.get_event_loop().create_future()
        self.pending_requests[request_id] = future
        
        await self.ws.send(json.dumps(request))
        
        try:
            result = await asyncio.wait_for(future, timeout=120)
            return result
        except asyncio.TimeoutError:
            self.pending_requests.pop(request_id, None)
            raise Exception("Request timeout")
    
    async def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupère l'historique de la session."""
        if not self.connected:
            await self.connect()
        
        result = await self._send_request("chat.history", {
            "sessionKey": SESSION_KEY,
            "limit": limit
        })
        
        if not result.get("ok"):
            return []
        
        return result.get("payload", {}).get("messages", [])
    
    async def send_message(self, message: str) -> str:
        """Envoie un message et attend la réponse."""
        if not self.connected:
            await self.connect()
        
        # Envoyer le message avec idempotencyKey
        result = await self._send_request("chat.send", {
            "sessionKey": SESSION_KEY,
            "message": message,
            "idempotencyKey": str(uuid.uuid4())
        })
        
        if not result.get("ok"):
            error = result.get("error", {})
            return f"Erreur: {error.get('message', 'Unknown error')}"
        
        # Attendre les événements de réponse
        full_response = ""
        
        try:
            while True:
                try:
                    event = await asyncio.wait_for(self.event_queue.get(), timeout=120)
                    
                    # Event de chat
                    if event.get("event") == "chat":
                        payload = event.get("payload", {})
                        
                        # Contenu textuel
                        if payload.get("kind") == "content":
                            full_response += payload.get("text", "")
                        
                        # Fin du message
                        if payload.get("kind") == "done":
                            break
                    
                except asyncio.TimeoutError:
                    break
        except Exception as e:
            if not full_response:
                return f"Erreur: {str(e)}"
        
        return full_response or "Message envoyé"
    
    async def close(self):
        """Ferme la connexion."""
        self.connected = False
        if self._listener_task:
            self._listener_task.cancel()
        if self.ws:
            await self.ws.close()


# Client singleton
_client: Optional[MoltbotClient] = None


async def get_client() -> MoltbotClient:
    global _client
    if _client is None:
        _client = MoltbotClient()
    return _client


async def chat_with_real_moltbot(message: str) -> str:
    """Envoie un message au vrai Moltbot."""
    try:
        client = await get_client()
        await client.connect()
        return await client.send_message(message)
    except Exception as e:
        return f"Erreur Moltbot: {str(e)}"


async def chat_with_gateway(
    message: str,
    gateway_url: str = GATEWAY_URL,
    token: str = GATEWAY_TOKEN,
    session_key: str = SESSION_KEY
) -> str:
    """Envoie un message via un Gateway Moltbot configurable."""
    try:
        # Créer un client temporaire avec les paramètres spécifiés
        client = MoltbotClient()
        client.gateway_url = gateway_url
        client.gateway_token = token
        client.session_key = session_key
        
        # Override les constantes pour ce client
        original_url = globals()['GATEWAY_URL']
        original_token = globals()['GATEWAY_TOKEN']
        original_session = globals()['SESSION_KEY']
        
        globals()['GATEWAY_URL'] = gateway_url
        globals()['GATEWAY_TOKEN'] = token
        globals()['SESSION_KEY'] = session_key
        
        try:
            await client.connect()
            return await client.send_message(message)
        finally:
            # Restaurer les valeurs originales
            globals()['GATEWAY_URL'] = original_url
            globals()['GATEWAY_TOKEN'] = original_token
            globals()['SESSION_KEY'] = original_session
            await client.close()
            
    except Exception as e:
        return f"Erreur Gateway: {str(e)}"


async def get_chat_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Récupère l'historique."""
    try:
        client = await get_client()
        await client.connect()
        return await client.get_history(limit)
    except Exception:
        return []
