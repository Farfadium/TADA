---
description: Configuration source Bear — extraction notes Markdown vers TADA
---

# Bear

> Application de notes Markdown — tags, wiki-links, écriture élégante.

**Type :** `notes`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [ ] API officielle (pas d'API REST)
- [x] MCP disponible (bear-mcp-server)
- [x] Export manuel (Markdown, HTML, PDF)
- [x] Scraping/autre (base SQLite, x-callback URLs)

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `bear-mcp-server` | Accès notes Bear | [GitHub](https://github.com/akseyh/bear-mcp-server) |
| `mcp-bear-notes` | MCP pour Bear | [GitHub](https://github.com/netologist/mcp-bear-notes) |

**MCP recommandé :** `bear-mcp-server`

**Prérequis :**
- macOS/iOS avec Bear
- Bear Pro (pour sync multi-device)

**Permissions :**
- [x] Lecture (via SQLite ou x-callback)
- [x] Écriture (via x-callback URLs)
- [ ] Suppression (trash)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Export manuel (le plus simple)**
1. Bear → File → Export Notes
2. Sélectionner Markdown
3. Inclure images
4. Sauvegarder dans `DATA/PENDING/bear/`

**Méthode 2 : Base SQLite**
```bash
# Localisation base (macOS)
DB="$HOME/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/database.sqlite"

# Export notes
sqlite3 "$DB" "SELECT ZTITLE, ZTEXT FROM ZSFNOTE WHERE ZTRASHED=0"
```

**Méthode 3 : x-callback-url**
```
bear://x-callback-url/open-note?id=xxx&show_window=no
bear://x-callback-url/search?term=tag:work
```

**Période recommandée :** Toutes les notes

**Destination :** `DATA/PENDING/bear/`

---

## Format des fichiers

**Structure :**
```
bear/
├── index.md                    # Index par tag
├── notes/
│   ├── Note-Title.md
│   └── ...
└── images/
    └── ...
```

**Format note Bear :**
```markdown
---
id: BEAR_UUID
title: Titre de la note
created: 2024-01-15T10:30:00Z
modified: 2024-07-15T14:22:00Z
tags: [work, project-x, ideas]
pinned: false
archived: false
---

# Titre de la note

#work #project-x #ideas

[Contenu de la note]

## Liens
[[Autre note liée]]
```

---

## Sync incrémentale

**Fréquence :** session

**Via SQLite :**
```sql
SELECT * FROM ZSFNOTE 
WHERE ZMODIFICATIONDATE > datetime('now', '-1 day')
  AND ZTRASHED = 0
```

**Critères :**
- Notes modifiées depuis dernière sync
- Nouvelles notes créées

---

## Actions disponibles

**Via x-callback-url :**
- `open-note` — Ouvrir une note
- `search` — Rechercher
- `create` — Créer note
- `add-text` — Ajouter contenu
- `add-file` — Ajouter fichier

**Exemples :**
```
bear://x-callback-url/create?title=Nouvelle&text=Contenu&tags=tag1,tag2
bear://x-callback-url/search?term=tag:work&show_window=no
```

---

## Mapping Bear → TADA

| Bear | TADA |
|------|------|
| Note | `DATA/ARCHIVE/Notes/` ou projet |
| Tag | Tag TADA |
| [[WikiLink]] | [[Lien TADA]] |
| Image | `_attachments/` |

---

## Tags Bear

**Format Bear :**
```
#tag
#multi-word tag#
#nested/tag
```

**Conversion TADA :**
- `#tag` → tag simple
- `#multi-word tag#` → tag avec espaces
- `#nested/tag` → hiérarchie tags

---

## Notes

**Avantages Bear :**
- Format Markdown natif
- Tags inline élégants
- WikiLinks [[supportés]]
- Export propre

**Limites :**
- macOS/iOS uniquement
- Pas d'API REST
- Bear Pro requis pour sync

**WikiLinks :**
- Bear supporte `[[liens]]`
- Directement compatible TADA
- Préserver lors de l'import

**Bonnes pratiques :**
- Export régulier en Markdown
- Garder les tags alignés avec TADA
- Bear = capture, TADA = archive

_Les configurations spécifiques sont dans `local/TOOLS.md`._
