---
description: Configuration source OneDrive — sync fichiers Microsoft cloud vers TADA
---

# OneDrive

> Stockage cloud Microsoft — fichiers, dossiers, intégration Office 365.

**Type :** `files`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Microsoft Graph API)
- [x] MCP disponible (officiel Microsoft)
- [x] Export manuel (dossier sync local)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `files-mcp-server` (Microsoft) | Officiel Microsoft | [GitHub](https://github.com/microsoft/files-mcp-server) |
| `mcp-onedrive-sharepoint` | OneDrive + SharePoint | [GitHub](https://github.com/ftaricano/mcp-onedrive-sharepoint) |

**MCP recommandé :** `files-mcp-server` (officiel Microsoft)

**Credentials nécessaires :**
- Azure AD App Registration
- Client ID + Client Secret
- Scopes : Files.Read, Files.ReadWrite

**Permissions :**
- [x] Lecture (fichiers, métadonnées)
- [x] Écriture (upload, création)
- [ ] Suppression (avec confirmation)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Dossier sync local**
```bash
# OneDrive synchronisé localement (macOS/Windows)
cp -r ~/OneDrive/* DATA/PENDING/onedrive/
```

**Méthode 2 : Via Microsoft Graph API**
```bash
# Lister fichiers racine
curl -X GET "https://graph.microsoft.com/v1.0/me/drive/root/children" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# Télécharger fichier
curl -X GET "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/content" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -o fichier.pdf
```

**Période recommandée :** Tout ou dossiers spécifiques

**Destination :** `DATA/PENDING/onedrive/`

---

## Format des fichiers

**Structure :**
```
onedrive/
├── index.md
├── Documents/
│   ├── file.docx
│   └── file.docx.md
└── ...
```

**Format métadonnées :**
```markdown
---
id: ITEM_ID
name: document.docx
webUrl: https://onedrive.live.com/...
size: 45678
createdDateTime: 2024-01-15T10:30:00Z
lastModifiedDateTime: 2024-07-15T14:22:00Z
createdBy: user@example.com
---

# document.docx

**Taille :** 45 KB
**Modifié :** 2024-07-15
**Lien :** [OneDrive](https://onedrive.live.com/...)

## Contenu
[Résumé si extrait]
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via delta API :**
```bash
# Delta pour changements
curl -X GET "https://graph.microsoft.com/v1.0/me/drive/root/delta" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

---

## Actions disponibles (via MCP)

**Lecture :**
- `list_children` — Lister contenu dossier
- `get_item` — Métadonnées fichier
- `download` — Télécharger
- `search` — Recherche

**Écriture :**
- `upload` — Uploader fichier
- `create_folder` — Créer dossier
- `move` — Déplacer

---

## Notes

**Intégration Office :**
- Documents Office éditables en ligne
- Export en différents formats possible

**SharePoint :**
- Même API (Graph) pour SharePoint
- Sites et bibliothèques accessibles

**Limites :**
- 429 Too Many Requests si abus
- Fichiers > 4 MB = upload session

_Les configurations spécifiques sont dans `local/TOOLS.md`._
