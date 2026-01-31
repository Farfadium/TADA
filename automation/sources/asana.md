---
description: Configuration source Asana — sync projets, tâches, équipes vers TADA
---

# Asana

> Gestion de projet d'équipe — projets, tâches, sections, timeline.

**Type :** `tasks` / `projects`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Asana REST API)
- [x] MCP disponible (mcp-server-asana)
- [x] Export manuel (CSV, JSON via UI)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `mcp-server-asana` | Complet | [GitHub](https://github.com/roychri/mcp-server-asana) |

**MCP recommandé :** `mcp-server-asana`

**Credentials nécessaires :**
- Personal Access Token : https://app.asana.com/0/my-apps
- Ou OAuth 2.0 pour applications

**Permissions :**
- [x] Lecture (projets, tâches, users)
- [x] Écriture (création, modification)
- [ ] Suppression (via API avec confirmation)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via MCP**
```bash
{
  "mcpServers": {
    "asana": {
      "command": "npx",
      "args": ["-y", "mcp-server-asana"],
      "env": {
        "ASANA_ACCESS_TOKEN": "xxx"
      }
    }
  }
}
```

**Méthode 2 : Export CSV**
1. Projet → Menu → Export → CSV
2. Ou utiliser l'API pour export complet

**Méthode 3 : Via API**
```bash
# Récupérer les tâches d'un projet
curl "https://app.asana.com/api/1.0/projects/{project_gid}/tasks" \
  -H "Authorization: Bearer $TOKEN"
```

**Période recommandée :** Projets actifs + archives récentes

**Destination :** `DATA/PENDING/asana/`

---

## Format des fichiers

**Structure :**
```
asana/
├── index.md
├── workspaces/
│   └── Workspace-Name/
│       ├── projects/
│       │   ├── Project-1/
│       │   │   ├── index.md
│       │   │   └── tasks/
│       │   │       └── Task-1.md
│       └── teams/
```

**Format tâche :**
```markdown
---
gid: TASK_GID
name: Titre de la tâche
project: Nom du projet
section: Nom de la section
assignee: user@example.com
due_on: 2024-07-20
completed: false
tags: [tag1, tag2]
permalink_url: https://app.asana.com/0/xxx/xxx
---

# Titre de la tâche

**Projet :** [[Projects/Nom]]
**Section :** In Progress
**Assigné :** [[Jean Dupont]]
**Échéance :** 2024-07-20

## Description
[Notes de la tâche]

## Sous-tâches
- [ ] Sous-tâche 1
- [x] Sous-tâche 2

## Commentaires
> Commentaire important
> — [[Prénom Nom]], 2024-07-15
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via API avec modified_since :**
```bash
curl "https://app.asana.com/api/1.0/tasks?project=$PROJECT_GID&modified_since=2024-07-15T00:00:00Z" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (temps réel via webhooks)
- [x] Polling API (avec modified_since)
- [ ] Sync manuelle uniquement

**Webhooks Asana (recommandé) :**
```bash
# Créer un webhook
POST https://app.asana.com/api/1.0/webhooks
Authorization: Bearer $TOKEN
Content-Type: application/json

{
  "data": {
    "resource": "PROJECT_GID",
    "target": "https://your-domain.com/webhook/asana"
  }
}
```

**Handshake webhook :**
```
# Asana envoie un header X-Hook-Secret
# Répondre avec le même header pour confirmer
```

**Events disponibles :**
- `added` / `changed` / `removed` / `deleted` / `undeleted`
- Resources : tasks, projects, stories, tags, sections

**Payload webhook :**
```json
{
  "events": [{
    "action": "changed",
    "resource": {
      "gid": "xxx",
      "resource_type": "task"
    },
    "change": {
      "field": "completed",
      "action": "changed"
    }
  }]
}
```

**Polling (alternative) :**
```bash
curl "https://app.asana.com/api/1.0/tasks?project=$GID&modified_since=$ISO_DATE" \
  -H "Authorization: Bearer $TOKEN"
```

**Setup requis :**
1. Créer webhook via API
2. Répondre au handshake avec X-Hook-Secret
3. Webhook nécessite HTTPS valide
4. Stocker le secret pour vérification des signatures

**Fréquence recommandée :**
- Webhooks : temps réel
- Polling : toutes les 5-15 minutes

---

## Actions disponibles (via MCP)

**Lecture :**
- `get_workspaces` — Lister workspaces
- `get_projects` — Projets d'un workspace
- `get_tasks` — Tâches d'un projet
- `get_task` — Détails tâche
- `search_tasks` — Recherche

**Écriture :**
- `create_task` — Créer tâche
- `update_task` — Modifier tâche
- `add_comment` — Ajouter commentaire
- `complete_task` — Marquer terminé

---

## Mapping Asana → TADA

| Asana | TADA |
|-------|------|
| Workspace | Organisation |
| Project | `DATA/NOW/[Projet]/` |
| Section | Statut |
| Task | `_tasks/` |
| Assignee | [[People/Nom]] |
| Tag | Tag TADA |

---

## Notes

**Limites API :**
- 1500 requêtes/minute par token
- Pagination avec offset/limit

**Particularités :**
- Les webhooks nécessitent un handshake
- Les subtasks sont des tâches séparées
- Les custom fields sont accessibles

**Bonnes pratiques :**
- Un webhook par projet important
- Utiliser les sections comme statuts
- Sync des projets actifs seulement

_Les configurations spécifiques sont dans `local/TOOLS.md`._
