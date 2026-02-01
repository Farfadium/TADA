---
description: Configuration source Linear — sync issues, projets, cycles vers TADA
---

# Linear

> Gestion de projet moderne — issues, projets, cycles, roadmaps.

**Type :** `tasks` / `projects`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Linear GraphQL API)
- [x] MCP disponible (plusieurs options)
- [x] Export manuel (CSV via UI)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `linear-mcp-server` (jerhadf) | Complet | [GitHub](https://github.com/jerhadf/linear-mcp-server) |
| `mcp-server-linearapp` | GraphQL wrapper | [GitHub](https://github.com/magarcia/mcp-server-linearapp) |
| `mcp-server-linear` | Issues et projets | [GitHub](https://github.com/mkusaka/mcp-server-linear) |

**MCP recommandé :** `linear-mcp-server` (jerhadf)

**Credentials nécessaires :**
- API Key : Settings → API → Personal API keys
- Ou OAuth pour apps

**Permissions :**
- [x] Lecture (issues, projects, teams)
- [x] Écriture (création, modification)
- [ ] Suppression (archivage préféré)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via MCP**
```bash
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@jerhadf/linear-mcp-server"],
      "env": {
        "LINEAR_API_KEY": "lin_api_xxx"
      }
    }
  }
}
```

**Méthode 2 : Via GraphQL API**
```graphql
query {
  issues(first: 100) {
    nodes {
      id
      title
      description
      state { name }
      assignee { name email }
      project { name }
    }
  }
}
```

**Période recommandée :** Issues actives + 6 mois

**Destination :** `DATA/PENDING/linear/`

---

## Format des fichiers

**Structure :**
```
linear/
├── index.md
├── teams/
│   └── Team-Name/
│       ├── projects/
│       │   └── Project-1/
│       │       ├── index.md
│       │       └── issues/
│       └── cycles/
```

**Format issue :**
```markdown
---
id: ISSUE_ID
identifier: TEAM-123
title: Titre de l'issue
state: In Progress
priority: 2
project: Nom du projet
team: Nom de l'équipe
assignee: user@example.com
labels: [bug, urgent]
estimate: 3
due_date: 2024-07-20
url: https://linear.app/team/issue/TEAM-123
---

# TEAM-123: Titre de l'issue

**État :** In Progress
**Priorité :** High (2)
**Projet :** [[Projects/Nom]]
**Assigné :** [[Jean Dupont]]
**Estimation :** 3 points

## Description
[Description Markdown de l'issue]

## Commentaires
> Commentaire
> — [[Prénom Nom]], 2024-07-15
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via GraphQL avec updatedAt :**
```graphql
query {
  issues(filter: { updatedAt: { gte: "2024-07-15" } }) {
    nodes { id title state { name } }
  }
}
```

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (temps réel)
- [x] Polling API (GraphQL avec filter updatedAt)
- [ ] Sync manuelle uniquement

**Webhooks Linear (recommandé) :**
```bash
# Créer un webhook via l'UI ou API
# Settings → API → Webhooks → Create webhook

# Ou via API GraphQL
mutation {
  webhookCreate(input: {
    url: "https://your-domain.com/webhook/linear"
    teamId: "xxx"
    label: "TADA sync"
    resourceTypes: ["Issue", "Comment", "Project"]
  }) {
    webhook { id }
  }
}
```

**Events disponibles :**
- `Issue` : create, update, remove
- `Comment` : create, update, remove
- `Project` : create, update, remove
- `Cycle` : create, update, remove
- `IssueLabel` : create, update, remove

**Payload webhook :**
```json
{
  "action": "update",
  "type": "Issue",
  "data": {
    "id": "xxx",
    "title": "Issue title",
    "state": {"name": "Done"}
  },
  "updatedFrom": {
    "state": {"name": "In Progress"}
  }
}
```

**Vérification signature :**
```javascript
const crypto = require('crypto');
const signature = crypto
  .createHmac('sha256', WEBHOOK_SECRET)
  .update(rawBody)
  .digest('hex');
// Comparer avec header Linear-Signature
```

**Polling (alternative) :**
```graphql
query {
  issues(filter: { updatedAt: { gte: "$LAST_SYNC" } }) {
    nodes { id title updatedAt }
  }
}
```

**Setup requis :**
1. Créer webhook dans Settings → API
2. Ou via mutation GraphQL
3. Stocker le secret pour vérification
4. Gérer les retries (Linear retry en cas d'échec)

**Fréquence recommandée :**
- Webhooks : temps réel
- Polling : toutes les 5-10 minutes

---

## Actions disponibles (via MCP)

**Lecture :**
- `get_issues` — Lister issues
- `get_issue` — Détails issue
- `get_projects` — Lister projets
- `get_teams` — Lister équipes
- `search` — Recherche globale

**Écriture :**
- `create_issue` — Créer issue
- `update_issue` — Modifier issue
- `add_comment` — Commenter
- `assign_issue` — Assigner

---

## Mapping Linear → TADA

| Linear | TADA |
|--------|------|
| Team | Organisation/équipe |
| Project | `DATA/NOW/[Projet]/` |
| Issue | `_issues/` ou `_tasks/` |
| Cycle | Sprint/période |
| Label | Tag TADA |
| Assignee | [[People/Nom]] |

---

## Notes

**API GraphQL :**
- Requêtes complexes possibles
- Pagination avec cursor
- Rate limit: 1500 req/heure

**Particularités :**
- Identifiants courts (TEAM-123)
- États personnalisables par équipe
- Intégration Git native

**Bonnes pratiques :**
- Un webhook par équipe/projet
- Sync issues actives seulement
- Utiliser les cycles pour le contexte temporel

_Les configurations spécifiques sont dans `local/TOOLS.md`._
