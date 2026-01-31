---
description: Configuration source Things 3 — sync tâches macOS/iOS, export via AppleScript/URL schemes
---

# Things 3

> Gestionnaire de tâches macOS/iOS — inbox, projets, zones, tags.

**Type :** `tasks`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [ ] API officielle (pas d'API REST)
- [x] MCP disponible (via AppleScript)
- [x] Export manuel (AppleScript, Things URLs)
- [x] Scraping/autre (base SQLite)

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `mcp-things3` | AppleScript + x-callback URLs | [GitHub](https://github.com/drjforrest/mcp-things3) |
| `things-mcp` | Intégration Claude Desktop | [GitHub](https://github.com/jimfilippou/things-mcp) |
| `things-mcp` (hald) | Lecture base Things | [GitHub](https://github.com/hald/things-mcp) |

**MCP recommandé :** `mcp-things3` (lecture + écriture)

**Credentials nécessaires :**
- macOS uniquement (AppleScript)
- Automation permissions pour Claude/Terminal
- Things 3 installé

**Permissions :**
- [x] Lecture (via AppleScript/SQLite)
- [x] Écriture (via x-callback URLs)
- [ ] Suppression (trash uniquement)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via MCP**
```bash
# Configurer dans Claude Desktop :
{
  "mcpServers": {
    "things3": {
      "command": "npx",
      "args": ["-y", "mcp-things3"]
    }
  }
}
```

**Méthode 2 : AppleScript direct**
```applescript
tell application "Things3"
  set allTodos to to dos of list "Anytime"
  repeat with t in allTodos
    log (name of t) & " | " & (project of t)
  end repeat
end tell
```

**Méthode 3 : Base SQLite (lecture seule)**
```bash
# Localisation de la base
DB="$HOME/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/Things Database.thingsdatabase/main.sqlite"

# Export des tâches
sqlite3 "$DB" "SELECT title, status FROM TMTask WHERE trashed=0"
```

**Période recommandée :** Tâches actives + logbook récent

**Destination :** `DATA/PENDING/things3/`

---

## Format des fichiers

**Structure :**
```
things3/
├── index.md                    # Vue d'ensemble
├── inbox.md                    # Tâches inbox
├── today.md                    # Tâches du jour
├── areas/
│   ├── Area-Name/
│   │   ├── index.md
│   │   └── projects/
│   │       └── Projet-1.md
└── logbook/
    └── YYYY-MM/
        └── completed.md
```

**Format tâche :**
```markdown
---
id: THINGS_UUID
title: Titre de la tâche
type: to-do
status: open
area: Nom de la zone
project: Nom du projet
tags: [tag1, tag2]
when: today
deadline: 2024-07-15
created: 2024-07-10
completed: null
---

# Titre de la tâche

**Zone :** [[Areas/Nom]]
**Projet :** [[Projects/Nom]]
**Tags :** #tag1 #tag2
**Échéance :** 2024-07-15

## Notes
[Contenu des notes si présentes]

## Checklist
- [ ] Item 1
- [ ] Item 2
```

**Format projet :**
```markdown
---
id: PROJECT_UUID
title: Nom du projet
type: project
area: Nom de la zone
status: open
when: null
deadline: 2024-08-01
tags: [tag1]
---

# Nom du projet

**Zone :** [[Areas/Nom]]
**Deadline :** 2024-08-01

## Description
[Notes du projet]

## Tâches
- [ ] [[tasks/Tâche 1]]
- [ ] [[tasks/Tâche 2]]
```

---

## Sync incrémentale

**Fréquence :** session (à chaque démarrage)

**Via AppleScript (modification récente) :**
```applescript
tell application "Things3"
  set recentTodos to to dos of list "Logbook" whose modification date > (current date) - 1 * days
end tell
```

**Via SQLite :**
```sql
SELECT * FROM TMTask 
WHERE userModificationDate > datetime('now', '-1 day')
  AND trashed = 0
```

**Critères :**
- Tâches modifiées depuis dernière sync
- Nouvelles tâches dans Inbox
- Tâches complétées (Logbook)

---

## Actions disponibles (via MCP/AppleScript)

**Lecture :**
- Lister inbox, today, upcoming
- Récupérer projets et zones
- Lire tâches avec notes et checklists
- Accéder au Logbook

**Écriture (via x-callback URLs) :**
```
things:///add?title=Tâche&notes=Description&when=today&tags=tag1,tag2
things:///add-project?title=Projet&area=Zone
```

**Modification :**
```
things:///update?id=UUID&completed=true
```

---

## Mapping Things 3 → TADA

| Things 3 | TADA |
|----------|------|
| Inbox | `DATA/INBOX/` |
| Today | Vue filtrée |
| Area | Catégorie de projets |
| Project | `DATA/NOW/[Projet]/` |
| Logbook | `DATA/ARCHIVE/` |

---

## Workflow recommandé

**Capture :**
1. Quick Entry Things → Inbox
2. Sync TADA → Récupère inbox
3. Router vers projets TADA

**Planification :**
- Things gère le "when" (today, evening, someday)
- TADA gère le contexte et les relations

**Archivage :**
- Tâche complétée → Logbook Things
- Sync → Archive dans TADA avec contexte

---

## Liens et relations

- Zones → Catégories de projets
- Projets → [[NOW/Projet]]
- Tags → Tags TADA
- Personnes (via tags) → [[People/Nom]]

---

## Notes

**Limites :**
- macOS uniquement (pas d'API web)
- AppleScript = permissions nécessaires
- Base SQLite = lecture seule recommandée

**URL Schemes utiles :**
```
things:///show?id=inbox
things:///show?id=today
things:///show?query=tag:urgent
things:///json?data=[...]   # Import JSON
```

**Alternatives pour sync :**
- `things-cli` (Python) pour scripts
- Shortcuts iOS pour automatisation mobile

**Particularités :**
- Les deadlines sont distinctes du "when"
- Les checklists sont dans les notes (format spécifique)
- L'historique Logbook est persistant

**Bonnes pratiques :**
- Garder Things comme capture rapide
- TADA pour le contexte enrichi
- Sync régulière pour cohérence

_Les configurations spécifiques (zones à surveiller) sont dans `local/TOOLS.md`._
