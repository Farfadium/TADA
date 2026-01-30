"""Configuration des runtimes disponibles pour TADA Web."""

RUNTIMES = {
    "moltbot": {
        "id": "moltbot",
        "label": "Moltbot (Telegram)",
        "description": "Conversation partagée avec Telegram, contexte complet",
        "type": "gateway",
        "gateway_url": "ws://127.0.0.1:18789",
        "gateway_token": "ef6c68e50f27b0c0aaa2b91e706480d9a3cde125fec8320149ecc59b6008500f",
        "session_key": "agent:main:main",
        "enabled": True,
    },
    "claude": {
        "id": "claude",
        "label": "Claude (indépendant)",
        "description": "Session web isolée, accès aux fichiers TADA",
        "type": "api",
        "enabled": True,
    },
    "moltbot-web": {
        "id": "moltbot-web", 
        "label": "Moltbot Web (session dédiée)",
        "description": "Session web séparée via Moltbot Gateway",
        "type": "gateway",
        "gateway_url": "ws://127.0.0.1:18789",
        "gateway_token": "ef6c68e50f27b0c0aaa2b91e706480d9a3cde125fec8320149ecc59b6008500f",
        "session_key": "agent:main:web",
        "enabled": True,
    },
}

DEFAULT_RUNTIME = "claude"


def get_runtime(runtime_id: str) -> dict:
    """Récupère la config d'un runtime."""
    return RUNTIMES.get(runtime_id, RUNTIMES[DEFAULT_RUNTIME])


def get_available_runtimes() -> list:
    """Liste les runtimes disponibles."""
    return [
        {"id": k, "label": v["label"], "description": v["description"], "type": v["type"]}
        for k, v in RUNTIMES.items()
        if v.get("enabled", True)
    ]
