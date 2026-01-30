---
A quoi sert ce fichier:
Guide de déploiement rapide pour TADA Web sur VPS
---

# 🚀 Déploiement TADA Web

## Étape 1 : Pousser le code sur le VPS

Le code est auto-sync via Git. Assure-toi que tous les changements sont committés et poussés :

```bash
cd /Users/yvanwibaux/Library/CloudStorage/GoogleDrive-yvan.wibaux@gmail.com/Mon\ Drive/TADA
git add .
git commit -m "feat: TADA Web avec capture rapide et analyse automatique"
git push
```

## Étape 2 : Se connecter au VPS

```bash
ssh root@100.120.155.10  # ou via Tailscale
```

## Étape 3 : Installer TADA Web

```bash
cd /root/TADA/_SYSTEM/runtime/web/deploy
chmod +x setup.sh
./setup.sh
```

Le script va demander un mot de passe. Entre ton mot de passe pour l'interface web.

## Étape 4 : Configurer le service

### 4.1 Générer la SECRET_KEY

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4.2 Éditer le service systemd

```bash
nano /etc/systemd/system/tada-web.service
```

Modifier les lignes suivantes :

```ini
Environment="TADA_SECRET_KEY=<clé_générée_étape_4.1>"
Environment="TADA_ADMIN_PASSWORD_HASH=<hash_affiché_par_setup.sh>"
Environment="OPENAI_API_KEY=<ta_clé_openai>"  # Pour analyse d'images + transcription audio
```

Sauvegarder avec `Ctrl+X`, `Y`, `Enter`.

## Étape 5 : Démarrer le service

```bash
systemctl daemon-reload
systemctl enable tada-web
systemctl start tada-web
systemctl status tada-web
```

## Étape 6 : Vérifier que ça fonctionne

```bash
curl http://localhost:8080/
```

Devrait retourner :
```json
{"name":"TADA Web API","version":"0.1.0","status":"running"}
```

## Étape 7 : Accéder à l'interface

Ouvre ton navigateur sur :
- **Backend API :** http://100.120.155.10:8080
- **Docs API :** http://100.120.155.10:8080/docs

Pour le frontend, deux options :

### Option A : Dev server (temporaire)
```bash
cd /root/TADA/_SYSTEM/runtime/web/frontend
npm run dev -- --host 0.0.0.0 --port 8081
```

Puis ouvre : http://100.120.155.10:8081

### Option B : Production avec nginx (recommandé)

```bash
# Build le frontend
cd /root/TADA/_SYSTEM/runtime/web/frontend
npm run build

# Installer nginx si nécessaire
apt install -y nginx

# Créer la config nginx
cat > /etc/nginx/sites-available/tada-web <<'EOF'
server {
    listen 8081;
    server_name _;

    root /root/TADA/_SYSTEM/runtime/web/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Activer la config
ln -sf /etc/nginx/sites-available/tada-web /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

## Logs

Voir les logs en temps réel :
```bash
journalctl -u tada-web -f
```

## Mise à jour

Après un changement de code :
```bash
cd /root/TADA
git pull  # Si pas auto-sync
systemctl restart tada-web
```

## Troubleshooting

### Le service ne démarre pas
```bash
journalctl -u tada-web -n 50
```

### Port déjà utilisé
```bash
lsof -i :8080
# Tuer le processus si nécessaire
```

### Problème de permissions
```bash
chown -R root:root /root/TADA/_SYSTEM/runtime/web
```

## ✅ Checklist

- [ ] Code poussé sur Git
- [ ] setup.sh exécuté
- [ ] SECRET_KEY générée et configurée
- [ ] ADMIN_PASSWORD_HASH configuré
- [ ] OPENAI_API_KEY configurée
- [ ] Service démarré : `systemctl status tada-web`
- [ ] Backend accessible : `curl http://localhost:8080/`
- [ ] Frontend accessible (dev ou nginx)
- [ ] Login fonctionne avec le mot de passe choisi
- [ ] Capture rapide fonctionne
- [ ] Photo/Audio fonctionnent avec analyse automatique

## Architecture finale

```
VPS (100.120.155.10) - Accessible uniquement via Tailscale
├── Moltbot (Discord/Telegram)
├── noVNC (port 6080)
└── TADA Web
    ├── Backend API (port 8080) — FastAPI + analyse AI
    └── Frontend (port 8081) — Svelte
```

Les fichiers capturés sont stockés dans `/root/TADA/DATA/PENDING/` et synchronisés automatiquement via Git.
