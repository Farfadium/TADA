---
A quoi sert ce fichier:
Instructions de déploiement de TADA Web sur le VPS
---

# Déploiement TADA Web

## Prérequis

- VPS avec Ubuntu/Debian
- Python 3.9+
- Git configuré avec auto-sync
- Tailscale configuré

## Installation

### 1. Sur le VPS

```bash
cd /root/TADA/_SYSTEM/runtime/web/deploy
chmod +x setup.sh
./setup.sh
```

Le script va :
- Créer le virtualenv Python
- Installer les dépendances backend
- Installer Node.js si nécessaire
- Installer les dépendances frontend
- Builder le frontend
- Copier le service systemd
- Générer le hash du mot de passe

### 2. Configuration du mot de passe

Après l'exécution du script, copier le hash généré dans `/etc/systemd/system/tada-web.service` :

```ini
Environment="TADA_ADMIN_PASSWORD_HASH=<hash_généré>"
```

### 3. Générer une SECRET_KEY

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Ajouter dans `/etc/systemd/system/tada-web.service` :

```ini
Environment="TADA_SECRET_KEY=<clé_générée>"
```

### 4. Configurer les API keys (optionnel mais recommandé)

Pour activer l'analyse automatique des fichiers (images et audio), ajouter dans `/etc/systemd/system/tada-web.service` :

```ini
Environment="ANTHROPIC_API_KEY=sk-ant-..."  # Pour analyse d'images (optionnel)
Environment="OPENAI_API_KEY=sk-..."         # Pour analyse d'images + transcription audio
```

**Note :** Le système utilise GPT-4 Vision (OpenAI) pour analyser les images et Whisper (OpenAI) pour transcrire l'audio. Sans ces clés, les fichiers sont quand même sauvegardés, mais sans analyse automatique.

### 5. Démarrer le service

```bash
systemctl daemon-reload
systemctl enable tada-web
systemctl start tada-web
systemctl status tada-web
```

## Accès

### Backend API
- URL: `http://100.120.155.10:8080` (via Tailscale)
- Docs: `http://100.120.155.10:8080/docs`

### Frontend
Le frontend est servi en mode dev pour le moment. Pour production :

```bash
cd /root/TADA/_SYSTEM/runtime/web/frontend
npm run build
# Servir le dossier dist/ avec nginx ou autre
```

## Logs

```bash
journalctl -u tada-web -f
```

## Mise à jour

Le code est auto-sync via Git. Pour redémarrer après une mise à jour :

```bash
systemctl restart tada-web
```

## Développement local

### Backend

```bash
cd _SYSTEM/runtime/web/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd _SYSTEM/runtime/web/frontend
npm install
npm run dev
```

L'API sera sur `http://localhost:8080`
Le frontend sur `http://localhost:8081`

## Architecture

```
VPS (100.120.155.10)
├── Moltbot (Discord/Telegram bot)
├── noVNC (port 6080) — Virtual desktop
└── TADA Web
    ├── Backend API (port 8080)
    └── Frontend (port 8081 dev, dist/ pour prod)
```

## Sécurité

- Accès uniquement via Tailscale (pas d'exposition publique)
- Auth JWT avec bcrypt pour les mots de passe
- Token valide 7 jours
- Pas de base de données (lecture/écriture directe des .md)

## TODO

- [ ] Configurer nginx pour servir le frontend en production
- [ ] Ajouter HTTPS via Tailscale Funnel (optionnel)
- [ ] Ajouter Progressive Web App (PWA) manifest pour mobile
- [ ] Configurer CORS pour restreindre à Tailscale uniquement
