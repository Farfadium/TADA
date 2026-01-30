---
A quoi sert ce fichier:
Documentation principale de TADA Web — Interface web pour capture rapide
---

# TADA Web

> Interface web minimaliste pour capturer et consulter TADA depuis n'importe où.

## Structure

```
web/
├── backend/          # API FastAPI
│   ├── main.py       # Point d'entrée
│   ├── config.py     # Configuration
│   ├── services.py   # Logique métier
│   └── requirements.txt
├── frontend/         # App Svelte
│   ├── src/
│   │   ├── App.svelte
│   │   └── components/
│   ├── package.json
│   └── vite.config.js
├── deploy/           # Scripts de déploiement
│   ├── setup.sh
│   ├── tada-web.service
│   └── README.md
└── .gitignore
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

API disponible sur http://localhost:8080
Docs auto sur http://localhost:8080/docs

### Frontend

Dans un autre terminal :

```bash
cd _SYSTEM/runtime/web/frontend
npm install
npm run dev
```

Interface disponible sur http://localhost:8081

### Login par défaut

En mode dev (sans `TADA_ADMIN_PASSWORD_HASH` configuré) :
- Username : `yvan`
- Password : n'importe quoi

## Fonctionnalités

### Dashboard
- Statistiques temps réel :
  - Nombre de projets actifs (NOW/)
  - Items en PENDING avec alerte > 7 jours
  - Dernière synchronisation git
- Liste des projets avec statut (🟢 🟡 🔴)
- Liste des items PENDING avec âge

### Quick Capture
- Champ texte pour capturer rapidement
- Détection automatique :
  - `@projet` → route vers NOW/projet/_inbox.md
  - `#tag` → extrait et ajoute en métadonnée
  - `[[lien]]` → détecte les liens wiki
- Routage intelligent :
  - Si 1 projet mentionné et existant → append dans le projet
  - Sinon → nouveau fichier dans PENDING/

### API

Endpoints principaux :

- `POST /auth/login` — Login et génération JWT
- `GET /dashboard` — Stats du dashboard
- `GET /projects` — Liste projets NOW/
- `GET /pending` — Liste items PENDING/
- `POST /capture` — Capture rapide

Voir http://localhost:8080/docs pour la doc complète.

## Déploiement

Voir [deploy/README.md](deploy/README.md) pour les instructions de déploiement sur le VPS.

## Architecture technique

### Backend
- **FastAPI** : Framework web Python moderne
- **JWT** : Authentification sans session
- **Bcrypt** : Hash des mots de passe
- **Pas de DB** : Lecture/écriture directe des fichiers .md

### Frontend
- **Svelte** : Framework JS léger et réactif
- **Vite** : Bundler ultra-rapide
- **Design** : Dark mode, minimaliste, mobile-friendly

### Sécurité
- Accès uniquement via Tailscale (pas d'exposition publique)
- Token JWT valide 7 jours
- 1 utilisateur pour le MVP (extensible)

## Prochaines étapes

- [ ] Déployer sur le VPS
- [ ] Tester la capture depuis mobile
- [ ] Ajouter PWA manifest pour installation mobile
- [ ] Configurer nginx pour production
- [ ] Ajouter visualisation graph (type Obsidian)
- [ ] Ajouter recherche fulltext
