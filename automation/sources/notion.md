---
description: Configuration source Notion — sync pages, bases de données, export workspace vers TADA
---

# Notion

> Workspace tout-en-un — notes, bases de données, wikis, projets.

**Type :** `notes` / `wiki`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Notion API)
- [x] MCP disponible (officiel Notion + communautaires)
- [x] Export manuel (Markdown, HTML, PDF)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| **Notion MCP (officiel)** | Serveur hébergé par Notion | [Docs](https://developers.notion.com/docs/mcp) |
| `notion-mcp` | Implémentation communautaire | [GitHub](https://github.com/ccabanillas/notion-mcp) |
| `mcp-server-notion` | Wrapper SDK officiel | [GitHub](https://github.com/ramidecodes/mcp-server-notion) |
| `notion-mcp-server` | Production-ready, complet | [GitHub](https://github.com/awkoy/notion-mcp-server) |

**MCP recommandé :** Notion MCP officiel (hébergé, pas besoin de self-host)

**Credentials nécessaires :**
- Notion Integration Token (Internal Integration)
- Ou OAuth 2.0 pour apps publiques

**Configuration Integration :**
1. Aller sur https://www.notion.so/my-integrations
2. Créer une nouvelle intégration
3. Copier le "Internal Integration Secret"
4. Partager les pages/DBs avec l'intégration

**Permissions :**
- [x] Lecture (pages, DBs, blocs)
- [x] Écriture (création, modification)
- [ ] Suppression (archive uniquement par défaut)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via API/MCP**
```bash
# Avec le MCP officiel, configurer dans Claude Desktop :
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": "secret_xxx"
      }
    }
  }
}
```

**Méthode 2 : Export manuel**
1. Settings & Members → Settings → Export all workspace content
2. Choisir format Markdown & CSV
3. Télécharger le ZIP
4. Extraire dans `DATA/PENDING/notion/`

**Période recommandée :** Tout le workspace

**Destination :** `DATA/PENDING/notion/`

---

## Format des fichiers

**Structure export :**
```
notion/
├── index.md                    # Index du workspace
├── pages/
│   ├── Page-Name-abc123.md
│   └── ...
├── databases/
│   ├── DB-Name-xyz789/
│   │   ├── _schema.md          # Structure de la DB
│   │   ├── Entry-1.md
│   │   └── Entry-2.md
│   └── ...
└── assets/
    └── images/
```

**Format page Notion :**
```markdown
---
id: PAGE_ID
title: Titre de la page
created: 2024-01-15T10:30:00Z
modified: 2024-06-20T14:22:00Z
parent: PARENT_PAGE_ID
icon: 📄
cover: https://...
url: https://notion.so/xxx
---

# Titre de la page

[Contenu de la page en Markdown]

## Propriétés (si dans une DB)
- **Status :** In Progress
- **Assignee :** [[Prénom Nom]]
- **Due Date :** 2024-07-01
```

**Format base de données :**
```markdown
---
id: DATABASE_ID
title: Nom de la base
created: 2024-01-15T10:30:00Z
properties:
  - name: Name
    type: title
  - name: Status
    type: select
    options: [Todo, In Progress, Done]
  - name: Assignee
    type: people
---

# Nom de la base

## Schema
| Propriété | Type | Options |
|-----------|------|---------|
| Name | title | — |
| Status | select | Todo, In Progress, Done |
| Assignee | people | — |
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via API :**
```javascript
// Rechercher les pages modifiées récemment
const results = await notion.search({
  filter: { property: 'object', value: 'page' },
  sort: { direction: 'descending', timestamp: 'last_edited_time' }
});
```

**Critères :**
- `last_edited_time > lastSyncDate`
- Nouvelles pages créées
- Modifications dans les DBs surveillées

---

## Actions disponibles (via MCP)

**Lecture :**
- `search` — Recherche dans le workspace
- `get_page` — Récupérer une page
- `get_database` — Récupérer structure DB
- `query_database` — Requêter une DB avec filtres
- `get_block_children` — Récupérer contenu

**Écriture :**
- `create_page` — Créer une page
- `update_page` — Modifier propriétés
- `append_block_children` — Ajouter du contenu
- `update_block` — Modifier un bloc

---

## Mapping Notion → TADA

| Notion | TADA |
|--------|------|
| Page simple | `DATA/ARCHIVE/Notes/` |
| Page projet | `DATA/NOW/[Projet]/` |
| DB Contacts | `DATA/ARCHIVE/Répertoires/People/` |
| DB Entreprises | `DATA/ARCHIVE/Répertoires/Orgs/` |
| Wiki/Docs | `DATA/ARCHIVE/Resources/` |

---

## Liens et relations

- Mentions de personnes → [[People/Nom]]
- Liens vers DBs entreprises → [[Orgs/Nom]]
- Références projets → [[NOW/Projet]]

---

## Notes

**Limites API :**
- 3 requêtes/seconde par intégration
- Blocks limités à 100 enfants par requête
- Fichiers/images via URLs temporaires (expirent)

**Particularités :**
- Les relations entre DBs sont préservées comme liens
- Les formules ne sont pas exportables (résultats seulement)
- Les rollups nécessitent requêtes supplémentaires

**Blocs non supportés en export Markdown :**
- Embeds (YouTube, etc.) → Garder l'URL
- Synced blocks → Résoudre avant export
- Database views → Exporter la DB source

**Bonnes pratiques :**
- Créer une intégration dédiée pour TADA
- Limiter l'accès aux pages nécessaires
- Utiliser les filtres pour sync incrémentale

_Les configurations spécifiques (token, DBs à surveiller) sont dans `local/TOOLS.md`._
