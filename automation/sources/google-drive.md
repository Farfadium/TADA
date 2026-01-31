---
description: Configuration source Google Drive — sync fichiers cloud, export documents, archivage dans projets
---

# Google Drive

> Stockage cloud Google — fichiers, dossiers, Google Docs/Sheets/Slides.

**Type :** `files`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Google Drive API v3)
- [x] MCP disponible (plusieurs options)
- [x] Export manuel (Google Takeout)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `@piotr-agier/google-drive-mcp` | Complet : Drive, Docs, Sheets, Slides | [GitHub](https://github.com/piotr-agier/google-drive-mcp) |
| `gdrive-mcp-server` | Lecture fichiers, navigation | [GitHub](https://github.com/felores/gdrive-mcp-server) |
| `mcp-gdrive` | Lecture Drive + édition Sheets | [GitHub](https://github.com/isaacphi/mcp-gdrive) |
| `google-docs-mcp` | Focus Docs/Sheets avec édition | [GitHub](https://github.com/a-bonus/google-docs-mcp) |

**MCP recommandé :** `@piotr-agier/google-drive-mcp` (le plus complet)

**Credentials nécessaires :**
- Google Cloud Project avec APIs activées :
  - Google Drive API
  - Google Docs API (optionnel)
  - Google Sheets API (optionnel)
- OAuth 2.0 Client ID (type Desktop)
- Fichier `gcp-oauth.keys.json`

**Permissions :**
- [x] Lecture (fichiers, métadonnées)
- [x] Écriture (upload, création)
- [ ] Suppression (désactivé par défaut)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via MCP**
```bash
# Installer le MCP
npm install -g @piotr-agier/google-drive-mcp

# Authentification (une seule fois)
npx @piotr-agier/google-drive-mcp auth

# Tokens stockés dans ~/.config/google-drive-mcp/tokens.json
```

**Méthode 2 : Google Takeout (export complet)**
1. Aller sur https://takeout.google.com
2. Sélectionner "Drive" uniquement
3. Choisir le format d'export (ZIP)
4. Télécharger et extraire

**Période recommandée :** Tout (pas de limite)

**Destination :** `DATA/PENDING/google-drive/`

---

## Format des fichiers

**Structure Drive :**
```
google-drive/
├── index.md                    # Index avec arborescence
├── My Drive/
│   ├── folder1/
│   │   ├── file1.pdf
│   │   └── file1.pdf.md       # Métadonnées + résumé
│   └── folder2/
└── Shared with me/
    └── ...
```

**Format métadonnées (fichier .md companion) :**
```markdown
---
id: DRIVE_FILE_ID
name: Nom du fichier.pdf
mimeType: application/pdf
size: 1234567
created: 2024-01-15T10:30:00Z
modified: 2024-06-20T14:22:00Z
owner: email@example.com
shared: true
webViewLink: https://drive.google.com/file/d/xxx/view
---

# Nom du fichier.pdf

**Type :** PDF Document
**Taille :** 1.2 MB
**Propriétaire :** [[Prénom Nom]]

## Résumé
[Description du contenu]

## Contexte
[Pourquoi ce fichier est important]
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via API/MCP :**
```javascript
// Récupérer les fichiers modifiés depuis dernière sync
const changes = await drive.changes.list({
  pageToken: lastSyncToken,
  fields: 'changes(file(id,name,mimeType,modifiedTime))'
});
```

**Critères :**
- `modifiedTime > lastSyncDate`
- Nouveaux fichiers partagés
- Fichiers ajoutés aux dossiers surveillés

---

## Actions disponibles (via MCP)

**Lecture :**
- `list_files` — Lister fichiers/dossiers
- `get_file` — Récupérer métadonnées
- `read_file` — Lire contenu (texte, Docs, Sheets)
- `search_files` — Recherche full-text

**Écriture :**
- `create_file` — Créer fichier/dossier
- `update_file` — Modifier contenu
- `upload_file` — Upload fichier local
- `move_file` — Déplacer fichier

**Google Docs/Sheets :**
- `create_doc` — Créer Google Doc
- `edit_doc` — Modifier document
- `read_sheet` — Lire données Sheets
- `update_sheet` — Modifier cellules

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (temps réel via Google Pub/Sub)
- [x] Polling API (changes.list avec pageToken)
- [ ] Sync manuelle uniquement

**Push Notifications (recommandé) :**
```bash
# Créer un watch sur les changements
POST https://www.googleapis.com/drive/v3/changes/watch
Authorization: Bearer $ACCESS_TOKEN
Content-Type: application/json

{
  "id": "unique-channel-id",
  "type": "web_hook",
  "address": "https://your-domain.com/webhook/drive",
  "expiration": "1735689600000"
}
```

**Events disponibles :**
- `sync` — Changement dans le Drive
- Header `X-Goog-Changed` : `content`, `properties`, `parents`
- Header `X-Goog-Resource-State` : `sync`, `add`, `remove`, `update`, `trash`

**Polling (alternative) :**
```bash
# Récupérer les changements depuis le dernier token
GET https://www.googleapis.com/drive/v3/changes?pageToken=$PAGE_TOKEN
Authorization: Bearer $ACCESS_TOKEN
```

**Setup requis :**
1. Domaine vérifié dans Google Cloud Console
2. Endpoint HTTPS accessible publiquement
3. Renouveler le watch avant expiration (max 24h pour Drive)
4. Stocker le `pageToken` pour le polling

**Fréquence recommandée :**
- Push : temps réel
- Polling : toutes les 5-15 minutes

---

## Liens et relations

- Fichiers partagés → [[People/Propriétaire]]
- Documents projet → `DATA/NOW/[Projet]/_drive/`
- Exports → attachments locaux

---

## Notes

**Formats natifs Google :**
- Google Docs → Exporter en .docx ou .md
- Google Sheets → Exporter en .xlsx ou .csv
- Google Slides → Exporter en .pptx ou .pdf

**Limites API :**
- 1000 requêtes/100 secondes/utilisateur
- 10 TB/jour de téléchargement
- Fichiers > 5MB nécessitent upload resumable

**Sécurité :**
- Ne jamais stocker les tokens OAuth en clair
- Vérifier les permissions de partage avant archivage
- Les fichiers partagés peuvent être révoqués

**Alternatives pour export massif :**
- `rclone` — Sync bidirectionnel efficace
- `gdrive` CLI — Export rapide

_Les configurations spécifiques (credentials, dossiers à surveiller) sont dans `local/TOOLS.md`._
