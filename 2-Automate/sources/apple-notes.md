---
description: Configuration source Apple Notes — extraction notes macOS/iCloud vers TADA
---

# Apple Notes

> Application de notes Apple — notes, dossiers, dessins, scans.

**Type :** `notes`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [ ] API officielle (pas d'API publique)
- [x] MCP disponible (mcp-apple-notes)
- [x] Export manuel (copier-coller, PDF)
- [x] Scraping/autre (AppleScript, base SQLite)

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `mcp-apple-notes` | RAG sur notes, indexation | [GitHub](https://github.com/RafalWilinski/mcp-apple-notes) |
| `apple-mcp` | Suite Apple (inclut Notes) | [GitHub](https://github.com/supermemoryai/apple-mcp) |
| `pyapple-mcp` | Python, multi-apps | [GitHub](https://github.com/54yyyu/pyapple-mcp) |

**MCP recommandé :** `mcp-apple-notes` (optimisé pour notes)

**Prérequis :**
- macOS avec Notes.app
- Permissions Automation accordées
- Notes sync iCloud (optionnel)

**Permissions :**
- [x] Lecture (via AppleScript)
- [x] Écriture (création notes)
- [ ] Suppression (avec confirmation)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via MCP**
```bash
{
  "mcpServers": {
    "apple-notes": {
      "command": "npx",
      "args": ["-y", "mcp-apple-notes"]
    }
  }
}
# Puis demander : "Index my notes"
```

**Méthode 2 : AppleScript**
```applescript
tell application "Notes"
  repeat with n in notes
    set noteTitle to name of n
    set noteBody to body of n
    set noteFolder to name of container of n
    log noteTitle & "|" & noteFolder & "|" & noteBody
  end repeat
end tell
```

**Méthode 3 : Base SQLite (avancé)**
```bash
# Localisation base
DB="$HOME/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite"

# Lecture (avec WAL checkpoint)
sqlite3 "$DB" "SELECT ZTITLE, ZSNIPPET FROM ZSFNOTE WHERE ZTRASHED=0"
```

**Période recommandée :** Toutes les notes ou dossiers spécifiques

**Destination :** `DATA/PENDING/apple-notes/`

---

## Format des fichiers

**Structure :**
```
apple-notes/
├── index.md                    # Index par dossier
├── Notes/                      # Dossier par défaut
│   ├── Note-Title.md
│   └── ...
├── Travail/
│   └── ...
└── attachments/
    ├── images/
    └── scans/
```

**Format note :**
```markdown
---
id: NOTE_UUID
title: Titre de la note
folder: Nom du dossier
created: 2024-01-15T10:30:00Z
modified: 2024-07-15T14:22:00Z
has_attachments: true
locked: false
---

# Titre de la note

**Dossier :** [[Folders/Nom]]
**Modifiée :** 2024-07-15

---

[Contenu de la note en Markdown]

## Pièces jointes
- [[attachments/image-001.jpg]]
- [[attachments/scan-001.pdf]]

## Checklist
- [ ] Item non coché
- [x] Item coché
```

---

## Sync incrémentale

**Fréquence :** session ou quotidien

**Via AppleScript :**
```applescript
tell application "Notes"
  set recentNotes to notes whose modification date > (current date) - 1 * days
end tell
```

**Via MCP :**
- Le MCP indexe les notes
- Détecte les changements à chaque query

---

## Actions disponibles (via MCP)

**Lecture :**
- `index_notes` — Indexer toutes les notes
- `search_notes` — Recherche sémantique
- `get_note` — Contenu d'une note
- `list_folders` — Lister dossiers

**Écriture :**
- `create_note` — Créer note
- `append_to_note` — Ajouter contenu

---

## Parsing du contenu

**Format interne Apple Notes :**
- HTML enrichi stocké en base
- Tables, checklists, dessins
- Pièces jointes inline

**Conversion en Markdown :**
```python
from bs4 import BeautifulSoup

def notes_html_to_md(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Convertir les éléments
    for checklist in soup.find_all('ul', class_='checklist'):
        # Traiter checklists
        pass
    return soup.get_text()
```

**Checklists :**
```html
<!-- Format Apple Notes -->
<ul class="checklist">
  <li data-checked="0">Non coché</li>
  <li data-checked="1">Coché</li>
</ul>

<!-- → Markdown -->
- [ ] Non coché
- [x] Coché
```

---

## Pièces jointes

**Types supportés :**
- Images (JPEG, PNG)
- Dessins (inline)
- Scans de documents
- PDFs
- URLs

**Extraction :**
```applescript
tell application "Notes"
  set noteAttachments to attachments of note "Ma Note"
  repeat with att in noteAttachments
    -- Extraire chaque attachment
  end repeat
end tell
```

---

## Détection nouvelles données

**Méthode disponible :**
- [ ] Webhook/Push (non disponible)
- [x] Polling API (SQLite ou AppleScript)
- [x] Sync manuelle uniquement

**Polling SQLite :**
```bash
DB="$HOME/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite"

# Notes modifiées récemment
sqlite3 "$DB" "
  SELECT ZTITLE, datetime(ZMODIFICATIONDATE + 978307200, 'unixepoch')
  FROM ZSFNOTE 
  WHERE ZMODIFICATIONDATE > (strftime('%s', 'now') - 978307200 - 3600)
    AND ZTRASHED = 0
"
```

**Polling AppleScript :**
```applescript
tell application "Notes"
  set recentNotes to notes whose modification date > (current date) - 1 * hours
  repeat with n in recentNotes
    log (id of n) & "|" & (name of n)
  end repeat
end tell
```

**Filesystem watch (détection indirecte) :**
```bash
# Surveiller le dossier Notes
fswatch -o "$HOME/Library/Group Containers/group.com.apple.notes" | while read; do
  echo "Notes database changed"
  # Déclencher sync
done
```

**Setup requis :**
1. Script cron/launchd pour polling
2. Ou watcher sur le dossier Group Containers
3. Stocker les derniers timestamps de modification

**Fréquence recommandée :**
- Polling : toutes les 15-30 minutes
- Filesystem watch : quasi temps réel

**Note :** Les notes protégées par mot de passe ne sont pas accessibles.

---

## Liens et relations

- Note projet → [[NOW/Projet]]
- Personnes mentionnées → [[People/Nom]]
- Scans documents → [[documents/...]]

---

## Notes

**Limites :**
- Pas d'API officielle
- AppleScript = permissions macOS
- Notes protégées = inaccessibles

**Notes protégées par mot de passe :**
- Non accessibles via API
- Déverrouiller manuellement si nécessaire

**Dessins et annotations :**
- Exportés en images
- Perdent l'aspect éditable

**Particularités :**
- Les notes sont en HTML enrichi
- Les tables sont supportées
- Les hashtags sont détectés

**Bonnes pratiques :**
- Indexer régulièrement
- Exporter les notes importantes manuellement
- Garder Apple Notes pour capture rapide

_Les configurations spécifiques sont dans `local/TOOLS.md`._
