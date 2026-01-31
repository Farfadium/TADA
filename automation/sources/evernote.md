---
description: Configuration source Evernote — migration notes vers TADA
---

# Evernote

> Application de notes historique — notebooks, tags, web clipper.

**Type :** `notes`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Evernote API, limitée)
- [x] MCP disponible (evernote-mcp-server)
- [x] Export manuel (ENEX, HTML)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `evernote-mcp-server` (brentmid) | Queries et recherche | [GitHub](https://github.com/brentmid/evernote-mcp-server) |
| `mcp-evernote` (verygoodplugins) | Sync et webhooks | [GitHub](https://github.com/verygoodplugins/mcp-evernote) |

**MCP recommandé :** `evernote-mcp-server` (brentmid)

**Credentials nécessaires :**
- Developer Token Evernote
- Ou OAuth (pour apps publiques)

**Permissions :**
- [x] Lecture (notes, notebooks, tags)
- [x] Écriture (création notes)
- [ ] Suppression (trash)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Export ENEX (recommandé pour migration)**
1. Evernote → Notebooks → clic droit → Export
2. Format ENEX
3. Convertir en Markdown avec `evernote2md`

```bash
# Installer convertisseur
go install github.com/wormi4ok/evernote2md@latest

# Convertir
evernote2md export.enex DATA/PENDING/evernote/
```

**Méthode 2 : Via MCP**
```bash
{
  "mcpServers": {
    "evernote": {
      "command": "npx",
      "args": ["-y", "evernote-mcp-server"],
      "env": {
        "EVERNOTE_TOKEN": "xxx"
      }
    }
  }
}
```

**Méthode 3 : Export HTML**
- Export notebook en HTML
- Convertir avec `pandoc`

**Période recommandée :** Tout (migration complète)

**Destination :** `DATA/PENDING/evernote/`

---

## Format des fichiers

**Structure :**
```
evernote/
├── index.md
├── notebooks/
│   ├── Notebook1/
│   │   ├── Note-Title.md
│   │   └── ...
│   └── ...
├── tags.md                     # Index des tags
└── attachments/
    └── ...
```

**Format note :**
```markdown
---
guid: NOTE_GUID
title: Titre de la note
notebook: Nom du notebook
tags: [tag1, tag2]
created: 2024-01-15T10:30:00Z
updated: 2024-07-15T14:22:00Z
source_url: https://...
---

# Titre de la note

**Notebook :** [[Notebooks/Nom]]
**Tags :** #tag1 #tag2

---

[Contenu converti en Markdown]

## Pièces jointes
- [[attachments/fichier.pdf]]
```

---

## Conversion ENEX → Markdown

**Format ENEX (XML) :**
```xml
<note>
  <title>Titre</title>
  <content><![CDATA[<?xml ...><en-note>HTML content</en-note>]]></content>
  <created>20240115T103000Z</created>
  <tag>tag1</tag>
  <resource>
    <data encoding="base64">...</data>
  </resource>
</note>
```

**Outils de conversion :**
| Outil | Langage | Lien |
|-------|---------|------|
| `evernote2md` | Go | [GitHub](https://github.com/wormi4ok/evernote2md) |
| `yarle` | Node.js | [GitHub](https://github.com/akosbalasko/yarle) |
| `enex2notion` | Python | Pour migration Notion |

---

## Sync incrémentale

**Fréquence :** Non recommandé (migration one-shot)

**Via API (si continué) :**
```python
# SDK Python
from evernote.api.client import EvernoteClient
client = EvernoteClient(token=TOKEN)
note_store = client.get_note_store()
notes = note_store.findNotesMetadata(filter, offset, max_notes, spec)
```

---

## Actions disponibles (via MCP)

**Lecture :**
- `search_notes` — Recherche
- `get_note` — Contenu note
- `list_notebooks` — Lister notebooks
- `list_tags` — Lister tags

**Écriture :**
- `create_note` — Créer note

---

## Mapping Evernote → TADA

| Evernote | TADA |
|----------|------|
| Notebook | Dossier ou catégorie |
| Note | `DATA/ARCHIVE/Notes/` |
| Tag | Tag TADA |
| Reminder | Pas de mapping (Evernote feature) |
| Web Clip | Source URL préservée |

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (via MCP evernote avec polling transformé)
- [x] Polling API (avec updateCount)
- [ ] Sync manuelle uniquement

**Polling avec updateCount :**
```python
from evernote.api.client import EvernoteClient

client = EvernoteClient(token=TOKEN)
note_store = client.get_note_store()

# getSyncState retourne updateCount
sync_state = note_store.getSyncState()
current_update_count = sync_state.updateCount

# Si updateCount a changé depuis la dernière sync
if current_update_count > last_update_count:
    # Récupérer les notes modifiées
    filter = NoteFilter()
    filter.order = NoteSortOrder.UPDATED
    notes = note_store.findNotes(filter, 0, 50)
```

**Via MCP avec webhook :**
```javascript
// Le MCP mcp-evernote peut envoyer des webhooks
// quand il détecte des changements via polling
{
  "webhook_url": "https://your-domain.com/webhook/evernote",
  "poll_interval": 300  // 5 minutes
}
```

**Setup requis :**
1. Developer token Evernote
2. Script polling régulier
3. Stocker updateCount et lastSyncTime

**Fréquence recommandée :**
- Polling : toutes les 15-30 minutes
- Evernote rate limits = prudence

**Note pour migration :**
Pour une migration one-shot, pas besoin de détection temps réel. Export ENEX complet puis conversion.

---

## Notes

**Limites API :**
- Developer tokens limités
- API rate limits stricts
- Pas de sync temps réel

**Migration recommandée :**
- Evernote → ENEX → Markdown → TADA
- One-shot plutôt que sync continue
- Vérifier les pièces jointes

**Particularités Evernote :**
- Format ENML (HTML modifié)
- Attachments encodés en base64
- Liens internes = `evernote:///`

**Bonnes pratiques :**
- Export complet avant migration
- Vérifier conversion des tables
- Préserver les métadonnées

_Les configurations spécifiques sont dans `local/TOOLS.md`._
