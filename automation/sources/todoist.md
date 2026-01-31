---
description: Configuration source Todoist — sync tâches, projets, capture inbox vers TADA
---

# Todoist

> Gestionnaire de tâches — inbox, projets, labels, rappels.

**Type :** `tasks`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Todoist REST & Sync API)
- [x] MCP disponible (officiel Doist)
- [x] Export manuel (CSV, JSON via UI)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| **Doist/todoist-ai** | Officiel Doist (actif) | [GitHub](https://github.com/Doist/todoist-ai) |
| `todoist-mcp-server` | Communautaire, complet | [GitHub](https://github.com/abhiz123/todoist-mcp-server) |
| `mcp-todoist` | Bulk operations | [GitHub](https://github.com/greirson/mcp-todoist) |
| `taskMaster-todoist-mcp` | Pour Cursor AI | [GitHub](https://github.com/mingolladaniele/taskMaster-todoist-mcp) |

**MCP recommandé :** `Doist/todoist-ai` (officiel, maintenu)

**Credentials nécessaires :**
- API Token Todoist
  - Settings → Integrations → Developer → API token

**Permissions :**
- [x] Lecture (tâches, projets, labels)
- [x] Écriture (création, modification)
- [x] Suppression (compléter, supprimer tâches)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via MCP**
```bash
# Configurer dans Claude Desktop :
{
  "mcpServers": {
    "todoist": {
      "command": "npx",
      "args": ["-y", "@doist/todoist-mcp"],
      "env": {
        "TODOIST_API_TOKEN": "xxx"
      }
    }
  }
}
```

**Méthode 2 : Via API directe**
```bash
# Récupérer toutes les tâches actives
curl -X GET "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"

# Récupérer tous les projets
curl -X GET "https://api.todoist.com/rest/v2/projects" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

**Méthode 3 : Export manuel**
1. Settings → Backups → Download
2. Format : ZIP contenant JSON

**Période recommandée :** Tâches actives + 6 mois d'historique

**Destination :** `DATA/PENDING/todoist/`

---

## Format des fichiers

**Structure :**
```
todoist/
├── index.md                    # Vue d'ensemble
├── inbox/
│   └── tasks.md                # Tâches inbox
├── projects/
│   ├── Projet-1/
│   │   ├── index.md
│   │   └── tasks.md
│   └── Projet-2/
└── completed/
    └── YYYY-MM/
        └── tasks.md
```

**Format tâche :**
```markdown
---
id: TASK_ID
content: Titre de la tâche
project_id: PROJECT_ID
project_name: Nom du projet
priority: 4
due_date: 2024-07-15
due_datetime: 2024-07-15T10:00:00Z
labels: [urgent, work]
created: 2024-07-10T08:30:00Z
completed: null
assignee: USER_ID
url: https://todoist.com/showTask?id=xxx
---

# Titre de la tâche

**Projet :** [[Projets/Nom du projet]]
**Priorité :** P1 🔴
**Échéance :** 2024-07-15
**Labels :** #urgent #work

## Description
[Contenu de la description si présente]

## Sous-tâches
- [ ] Sous-tâche 1
- [ ] Sous-tâche 2

## Commentaires
[Commentaires si présents]
```

---

## Sync incrémentale

**Fréquence :** session (à chaque démarrage)

**Via Sync API :**
```bash
# Sync incrémentale avec token
curl -X POST "https://api.todoist.com/sync/v9/sync" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -d "sync_token=*" \
  -d "resource_types=[\"items\",\"projects\"]"
```

**Critères :**
- Tâches modifiées/créées depuis dernier sync_token
- Tâches complétées récemment
- Changements de projets/labels

---

## Actions disponibles (via MCP)

**Lecture :**
- `get_tasks` — Lister tâches (avec filtres)
- `get_task` — Détails d'une tâche
- `get_projects` — Lister projets
- `get_labels` — Lister labels
- `search_tasks` — Recherche

**Écriture :**
- `create_task` — Créer tâche
- `update_task` — Modifier tâche
- `complete_task` — Marquer comme fait
- `create_project` — Créer projet

**Bulk :**
- `batch_create_tasks` — Créer plusieurs tâches
- `move_tasks` — Déplacer vers projet

---

## Mapping Todoist → TADA

| Todoist | TADA |
|---------|------|
| Inbox | `DATA/INBOX/` (à trier) |
| Projet actif | `DATA/NOW/[Projet]/_tasks/` |
| Projet archivé | `DATA/ARCHIVE/Projects/` |
| Tâche complétée | Reste dans le projet, marquée ✅ |

---

## Workflow recommandé

**Capture :**
1. Tâches entrantes → Inbox Todoist
2. Sync TADA → Récupère inbox
3. L'IA propose de router vers projets

**Archivage :**
1. Tâche complétée dans Todoist
2. Sync → Mise à jour dans TADA
3. Contexte préservé dans le projet

**Bidirectionnel :**
- Créer tâche dans TADA → Push vers Todoist
- Compléter dans Todoist → Update dans TADA

---

## Liens et relations

- Tâches assignées → [[People/Assigné]]
- Projets → [[NOW/Projet]]
- Labels → Tags TADA

---

## Notes

**Limites API :**
- REST: 450 requêtes/15 min
- Sync: Plus permissif, utiliser sync_token

**Particularités :**
- Les priorités sont inversées (4 = P1, 1 = P4)
- Les rappels ne sont pas dans l'API REST
- Les commentaires nécessitent Premium

**Natural Language :**
- L'API parse le langage naturel (dates, priorités)
- Exemple : "Appeler Jean demain à 10h p1"

**Bonnes pratiques :**
- Utiliser sync_token pour l'incrémental
- Ne pas supprimer, juste compléter
- Garder les projets alignés avec TADA

_Les configurations spécifiques (token, projets surveillés) sont dans `local/TOOLS.md`._
