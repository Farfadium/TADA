---
description: Configuration source Google Contacts — sync contacts Gmail/Workspace vers People/
---

# Google Contacts

> Carnet d'adresses Google — contacts, groupes, synchronisé avec Gmail/Workspace.

**Type :** `contacts`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (People API)
- [x] MCP disponible (google-workspace-mcp)
- [x] Export manuel (Google Contacts → CSV/vCard)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `google-workspace-mcp` | Gmail + Calendar + Drive + Contacts | [GitHub](https://github.com/aaronsb/google-workspace-mcp) |
| MCP Google officiel | Dans le référentiel MCP | [GitHub](https://github.com/modelcontextprotocol/servers) |

**MCP recommandé :** `google-workspace-mcp` (tout-en-un Google)

**Credentials nécessaires :**
- Google Cloud Project avec People API activée
- OAuth 2.0 Client ID
- Scopes requis :
  - `https://www.googleapis.com/auth/contacts.readonly`
  - `https://www.googleapis.com/auth/contacts` (pour écriture)

**Permissions :**
- [x] Lecture (contacts, groupes)
- [x] Écriture (création, modification)
- [ ] Suppression (avec confirmation)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via MCP**
```bash
# Configurer dans Claude Desktop :
{
  "mcpServers": {
    "google-workspace": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "~/.mcp/google-workspace-mcp:/app/config",
        "-e", "GOOGLE_CLIENT_ID",
        "-e", "GOOGLE_CLIENT_SECRET",
        "ghcr.io/aaronsb/google-workspace-mcp:latest"
      ],
      "env": {
        "GOOGLE_CLIENT_ID": "xxx.apps.googleusercontent.com",
        "GOOGLE_CLIENT_SECRET": "xxx"
      }
    }
  }
}
```

**Méthode 2 : Export manuel**
1. Aller sur https://contacts.google.com
2. Menu ≡ → Export
3. Choisir Google CSV ou vCard
4. Télécharger dans `DATA/PENDING/google-contacts/`

**Méthode 3 : Via API directe**
```bash
# Récupérer tous les contacts
curl -X GET "https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses,phoneNumbers,organizations" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Période recommandée :** Tous les contacts

**Destination :** `DATA/PENDING/google-contacts/`

---

## Format des fichiers

**Structure :**
```
google-contacts/
├── index.md                    # Index alphabétique
├── labels/
│   ├── Travail.md
│   ├── Amis.md
│   └── ...
└── contacts/
    ├── A/
    │   ├── Alice-Dupont.md
    │   └── ...
    └── ...
```

**Format contact :**
```markdown
---
resourceName: people/c123456789
etag: "%EgYBAj..."
names:
  - givenName: Prénom
    familyName: Nom
    displayName: Prénom Nom
emails:
  - value: pro@example.com
    type: work
  - value: perso@gmail.com
    type: home
phones:
  - value: +33612345678
    type: mobile
organizations:
  - name: Entreprise
    title: Poste
addresses:
  - formattedValue: "123 Rue, 75001 Paris"
    type: home
birthdays:
  - date:
      year: 1990
      month: 5
      day: 15
memberships:
  - contactGroupMembership:
      contactGroupId: label123
      contactGroupResourceName: contactGroups/label123
---

# Prénom Nom

**Entreprise :** [[Orgs/Entreprise]]
**Poste :** Poste

## Contact

| Type | Valeur |
|------|--------|
| 📧 Work | pro@example.com |
| 📧 Home | perso@gmail.com |
| 📱 Mobile | +33 6 12 34 56 78 |

## Adresse
123 Rue, 75001 Paris

## Labels
- Travail
- Clients

## Relations TADA
- Projets : [[NOW/Projet]]
- Emails : voir [[emails/2024/...]]
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via People API :**
```bash
# Utiliser syncToken pour l'incrémental
curl -X GET "https://people.googleapis.com/v1/people/me/connections?syncToken=$SYNC_TOKEN&personFields=names,emailAddresses" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Critères :**
- Contacts modifiés depuis dernier syncToken
- Nouveaux contacts
- Contacts supprimés (via requestSyncToken)

---

## Actions disponibles (via MCP/API)

**Lecture :**
- `people.connections.list` — Lister tous les contacts
- `people.get` — Détails d'un contact
- `people.searchContacts` — Recherche
- `contactGroups.list` — Lister les labels

**Écriture :**
- `people.createContact` — Créer contact
- `people.updateContact` — Modifier contact
- `people.deleteContact` — Supprimer contact
- `contactGroups.members.modify` — Gérer labels

---

## Mapping Google Contacts → TADA

| Google Contacts | TADA |
|-----------------|------|
| Contact | `DATA/ARCHIVE/Répertoires/People/` |
| Label (contactGroup) | Tag sur la fiche |
| Organization | `DATA/ARCHIVE/Répertoires/Orgs/` |
| Notes (biographies) | Section notes fiche |

---

## Synergies avec Gmail

**Enrichissement automatique :**
- Contact créé depuis email → Lien vers thread
- Emails récents → Historique dans fiche TADA

**Workflow :**
1. Nouvel email de contact inconnu
2. Création contact dans Google Contacts
3. Sync TADA → Fiche People créée
4. Emails archivés liés à la fiche

---

## Détection nouvelles données

**Méthode disponible :**
- [ ] Webhook/Push (non disponible pour People API)
- [x] Polling API (avec syncToken)
- [ ] Sync manuelle uniquement

**Polling avec syncToken (recommandé) :**
```bash
# Première requête : récupérer tous les contacts + syncToken
GET https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses&requestSyncToken=true
Authorization: Bearer $ACCESS_TOKEN

# Réponse inclut: "nextSyncToken": "xxx"

# Requêtes suivantes : utiliser syncToken
GET https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses&syncToken=$SYNC_TOKEN
```

**Réponse sync :**
```json
{
  "connections": [
    {
      "resourceName": "people/c123",
      "metadata": {
        "deleted": false  // true si contact supprimé
      }
    }
  ],
  "nextSyncToken": "new_token"
}
```

**Setup requis :**
1. Stocker le syncToken après chaque sync
2. Script cron pour polling régulier
3. Gérer les contacts supprimés (metadata.deleted)

**Fréquence recommandée :**
- Polling : toutes les 30 minutes à 1 heure
- Les contacts changent peu fréquemment

**Note :** Google Contacts n'a pas de webhook. Utiliser le syncToken est la méthode officielle pour l'incrémental.

---

## Liens et relations

- Organisation → [[Orgs/Entreprise]]
- Fiche TADA → [[People/Prénom Nom]]
- Labels → Tags TADA
- Emails → [[emails/...]]

---

## Notes

**Limites API :**
- 90 requêtes/minute pour connections.list
- 600 requêtes/minute pour get/update
- 60 contacts max par batch

**Différence People API vs Contacts API :**
- Contacts API (deprecated) → utiliser People API
- People API = API actuelle pour contacts

**Formats d'export :**
- Google CSV : format propriétaire, complet
- Outlook CSV : compatible Microsoft
- vCard : standard, portable

**Particularités :**
- Les photos sont en URLs temporaires
- Les contacts "Directory" (Workspace) sont séparés
- Les suggestions de contacts ne sont pas exportables

**Bonnes pratiques :**
- Utiliser syncToken pour l'incrémental
- Fusionner avec Folk/Apple Contacts selon le workflow
- Google = source pour contacts professionnels Gmail

_Les configurations spécifiques (credentials, labels surveillés) sont dans `local/TOOLS.md`._
