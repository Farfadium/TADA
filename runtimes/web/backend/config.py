"""Configuration pour TADA Web backend."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Chemins
# __file__ = _SYSTEM/runtime/web/backend/config.py
# On remonte 5 fois pour arriver à la racine TADA, ou on utilise TADA_ROOT_PATH si défini
TADA_ROOT = Path(os.getenv("TADA_ROOT_PATH", Path(__file__).parent.parent.parent.parent.parent)).resolve()
DATA_DIR = TADA_ROOT / "DATA"
SYSTEM_DIR = TADA_ROOT / "_SYSTEM"

NOW_DIR = DATA_DIR / "NOW"
PENDING_DIR = DATA_DIR / "PENDING"
ARCHIVE_DIR = DATA_DIR / "ARCHIVE"
MEMORY_DIR = DATA_DIR / "memory"

# Sécurité
SECRET_KEY = os.getenv("TADA_SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 jours

# API
API_HOST = os.getenv("TADA_API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("TADA_API_PORT", "8080"))

# Auth simple (pour MVP, un seul utilisateur)
ADMIN_USERNAME = os.getenv("TADA_ADMIN_USER", "yvan")
ADMIN_PASSWORD_HASH = os.getenv("TADA_ADMIN_PASSWORD_HASH", "")  # À générer

# API Keys pour analyse de contenu
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
