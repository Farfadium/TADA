---
description: Configuration source Trello — sync boards, cards, listes vers TADA
---

# Trello

> Gestion de projet visuelle — boards, listes, cartes, checklists.

**Type :** `tasks` / `projects`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Trello REST API)
- [x] MCP disponible (mcp-server-trello)
- [x] Export manuel (JSON via UI)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `mcp-server-trello` (delorenj) | Complet avec rate limiting | [GitHub](https://github.com/delorenj/mcp-server-trello) |
| `claude-mcp-trello` | Basique | [GitHub](https://github.com/hrs-asano/claude-mcp-trello) |

**MCP recommandé :** `mcp-server-trello` (delorenj)

**Credentials nécessaires :**
- API Key : https://trello.com/app-key
- Token : Généré via OAuth ou lien d'autorisation

**Permissions :**
- [x] Lecture (boards, cards, members)
- [x] Écriture (création, modification)
- [ ] Suppression (archivage préféré)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via MCP**
```bash
{
  "mcpServers": {
    "trello": {
      "command": "npx",
      "args": ["-y", "@delorenj/mcp-server-trello"],
      "env": {
        "TRELLO_API_KEY": "xxx",
        "TRELLO_TOKEN": "xxx"
      }
    }
  }
}
```

**Méthode 2 : Export JSON**
1. Board → Menu → More → Print and Export → Export as JSON
2. Sauvegarder dans `DATA/PENDING/trello/`

**Méthode 3 : Via API**
```bash
# Récupérer un board complet
curl "https://api.trello.com/1/boards/{boardId}?key=$KEY&token=$TOKEN&cards=all&lists=all"
```

**Période recommandée :** Boards actifs

**Destination :** `DATA/PENDING/trello/`

---

## Format des fichiers

**Structure :**
```
trello/
├── index.md
├── boards/
│   ├── Board-Name/
│   │   ├── index.md
│   │   ├── List-1.md
│   │   └── cards/
│   │       ├── Card-1.md
│   │       └── ...
```

**Format carte :**
```markdown
---
id: CARD_ID
name: Titre de la carte
list: Nom de la liste
board: Nom du board
due: 2024-07-20T10:00:00Z
labels: [urgent, feature]
members: [user1, user2]
url: https://trello.com/c/xxx
---

# Titre de la carte

**Liste :** [[Lists/Nom]]
**Board :** [[Boards/Nom]]
**Échéance :** 2024-07-20
**Membres :** [[Jean Dupont]], [[Marie Martin]]

## Description
[Contenu de la description]

## Checklist
- [ ] Item 1
- [x] Item 2

## Commentaires
> Commentaire important
> — [[Prénom Nom]], 2024-07-15
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via API avec since :**
```bash
# Actions récentes sur un board
curl "https://api.trello.com/1/boards/{boardId}/actions?key=$KEY&token=$TOKEN&since=2024-07-15"
```

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (temps réel)
- [x] Polling API (actions avec filter)
- [ ] Sync manuelle uniquement

**Webhooks Trello (recommandé) :**
```bash
# Créer un webhook
POST https://api.trello.com/1/webhooks?key=$KEY&token=$TOKEN
Content-Type: application/json

{
  "callbackURL": "https://your-domain.com/webhook/trello",
  "idModel": "BOARD_ID",
  "description": "TADA sync webhook"
}
```

**Events disponibles :**
- `createCard` / `updateCard` / `deleteCard`
- `addMemberToCard` / `removeMemberFromCard`
- `addChecklistToCard` / `updateCheckItemStateOnCard`
- `createList` / `updateList`
- `addAttachmentToCard`
- `commentCard`

**Payload webhook :**
```json
{
  "action": {
    "type": "updateCard",
    "data": {
      "card": {"id": "xxx", "name": "Card Name"},
      "list": {"id": "xxx", "name": "Done"}
    }
  }
}
```

**Polling (alternative) :**
```bash
# Actions depuis une date
curl "https://api.trello.com/1/boards/{id}/actions?since=$LAST_SYNC&key=$KEY&token=$TOKEN"
```

**Setup requis :**
1. Créer webhook via API (pas d'UI)
2. Endpoint HTTPS avec HEAD support
3. Trello envoie HEAD pour vérifier avant POST

**Fréquence recommandée :**
- Webhooks : temps réel
- Polling : toutes les 5-15 minutes

---

## Actions disponibles (via MCP)

**Lecture :**
- `get_boards` — Lister boards
- `get_lists` — Listes d'un board
- `get_cards` — Cartes d'une liste
- `get_card` — Détails carte
- `search` — Recherche globale

**Écriture :**
- `create_card` — Créer carte
- `update_card` — Modifier carte
- `move_card` — Déplacer vers liste
- `add_comment` — Ajouter commentaire

---

## Mapping Trello → TADA

| Trello | TADA |
|--------|------|
| Board | Projet ou catégorie |
| List | Statut (Todo, In Progress, Done) |
| Card | Tâche dans `_tasks/` |
| Member | [[People/Nom]] |
| Label | Tag |

---

## Notes

**Limites API :**
- 100 requêtes/10 secondes par token
- 300 requêtes/10 secondes par IP
- Rate limiting automatique dans le MCP

**Particularités :**
- Les webhooks nécessitent HEAD + POST
- Les dates sont en UTC
- Les pièces jointes ont des URLs temporaires

**Bonnes pratiques :**
- Un webhook par board important
- Archiver les cartes plutôt que supprimer
- Garder les boards alignés avec projets TADA

_Les configurations spécifiques sont dans `local/TOOLS.md`._
