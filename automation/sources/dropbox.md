---
description: Configuration source Dropbox — sync fichiers cloud, export documents vers TADA
---

# Dropbox

> Stockage cloud — fichiers, dossiers, partage, Paper.

**Type :** `files`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Dropbox API v2)
- [x] MCP disponible (plusieurs options)
- [x] Export manuel (dossier sync local, download ZIP)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `dropbox-mcp-server` (ngs) | Go, complet | [GitHub](https://github.com/ngs/dropbox-mcp-server) |
| `dbx-mcp-server` | Basique | [GitHub](https://github.com/amgadabdelhafez/dbx-mcp-server) |
| `dropbox-mcp-server-by-cdata` | Read-only, JDBC | [GitHub](https://github.com/CDataSoftware/dropbox-mcp-server-by-cdata) |

**MCP recommandé :** `dropbox-mcp-server` (ngs)

**Credentials nécessaires :**
- App Dropbox (https://www.dropbox.com/developers)
- Access Token ou OAuth 2.0
- Scopes : files.content.read, files.metadata.read

**Permissions :**
- [x] Lecture (fichiers, métadonnées)
- [x] Écriture (upload, création)
- [ ] Suppression (désactivé par défaut)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Dossier sync local (le plus simple)**
```bash
# Le dossier Dropbox synchronisé localement
cp -r ~/Dropbox/* DATA/PENDING/dropbox/
```

**Méthode 2 : Via API**
```bash
# Lister fichiers
curl -X POST https://api.dropboxapi.com/2/files/list_folder \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path": ""}'

# Télécharger fichier
curl -X POST https://content.dropboxapi.com/2/files/download \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Dropbox-API-Arg: {\"path\": \"/fichier.pdf\"}" \
  -o fichier.pdf
```

**Période recommandée :** Tout ou dossiers spécifiques

**Destination :** `DATA/PENDING/dropbox/`

---

## Format des fichiers

**Structure :**
```
dropbox/
├── index.md                    # Index arborescence
├── folder1/
│   ├── file.pdf
│   └── file.pdf.md            # Métadonnées
└── folder2/
    └── ...
```

**Format métadonnées :**
```markdown
---
id: id:xxx
name: document.pdf
path_display: /Folder/document.pdf
size: 1234567
content_hash: xxx
client_modified: 2024-07-15T10:30:00Z
server_modified: 2024-07-15T10:32:00Z
rev: 015e...
---

# document.pdf

**Chemin :** /Folder/document.pdf
**Taille :** 1.2 MB
**Modifié :** 2024-07-15

## Contenu
[Résumé du contenu si extrait]
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via API (cursor) :**
```bash
# Sync avec cursor
curl -X POST https://api.dropboxapi.com/2/files/list_folder/continue \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cursor": "$CURSOR"}'
```

**Via sync locale :**
- Le client Dropbox synchronise automatiquement
- Détecter les fichiers modifiés par date

---

## Actions disponibles (via MCP/API)

**Lecture :**
- `list_folder` — Lister contenu
- `download` — Télécharger fichier
- `get_metadata` — Métadonnées
- `search_v2` — Recherche full-text

**Écriture :**
- `upload` — Uploader fichier
- `create_folder_v2` — Créer dossier
- `move_v2` — Déplacer fichier

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (temps réel)
- [x] Polling API (list_folder/continue avec cursor)
- [ ] Sync manuelle uniquement

**Webhooks Dropbox (recommandé) :**
```bash
# 1. Configurer webhook dans App Console
# URL: https://your-domain.com/webhook/dropbox

# 2. Vérification (GET)
GET /webhook?challenge=xxx
# Répondre avec le challenge en plain text

# 3. Réception notification (POST)
POST /webhook
{
  "list_folder": {
    "accounts": ["dbid:AAH4f99..."]
  },
  "delta": {
    "users": [123456789]
  }
}
```

**Workflow webhook :**
1. Dropbox envoie notification (user IDs seulement)
2. Appeler `/files/list_folder/continue` avec le cursor stocké
3. Traiter les changements retournés

**Polling avec cursor :**
```bash
# Première requête
POST https://api.dropboxapi.com/2/files/list_folder
{"path": "", "recursive": true}
# Stocker le cursor de la réponse

# Requêtes suivantes
POST https://api.dropboxapi.com/2/files/list_folder/continue
{"cursor": "$CURSOR"}
```

**Long polling (alternative) :**
```bash
# Attendre jusqu'à 30s pour des changements
POST https://notify.dropboxapi.com/2/files/list_folder/longpoll
{"cursor": "$CURSOR", "timeout": 30}
```

**Setup requis :**
1. Configurer webhook URL dans App Console
2. Implémenter vérification challenge
3. Stocker cursor par utilisateur
4. Appeler list_folder/continue à chaque notification

**Fréquence recommandée :**
- Webhooks : temps réel
- Long polling : connexion persistante
- Polling classique : toutes les 5 minutes

---

## Notes

**Limites API :**
- 5000 appels/jour pour apps
- Fichiers > 150 MB = upload chunked

**Dropbox Paper :**
- Export en Markdown ou DOCX
- API séparée pour Paper

**Alternatives :**
- `rclone` pour sync bidirectionnelle efficace
- Client desktop pour sync continue

_Les configurations spécifiques sont dans `local/TOOLS.md`._
