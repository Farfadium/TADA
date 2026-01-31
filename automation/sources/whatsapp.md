---
description: Configuration source WhatsApp — archivage conversations, extraction médias, sync avec TADA
---

# WhatsApp

> Messagerie instantanée — conversations, groupes, médias, appels.

**Type :** `messaging`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [ ] API officielle (Business API uniquement, payante)
- [x] MCP disponible (plusieurs options)
- [x] Export manuel (export chat intégré)
- [x] Scraping/autre (WhatsApp Web, bases locales)

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `whatsapp-mcp` (lharries) | Python, lecture + envoi | [GitHub](https://github.com/lharries/whatsapp-mcp) |
| `wweb-mcp` | Node.js, WhatsApp Web | [GitHub](https://github.com/pnizer/wweb-mcp) |
| `mcp-whatsapp-web` | TypeScript, complet | [GitHub](https://github.com/mario-andreschak/mcp-whatsapp-web) |
| `whatsapp-mcp-ts` | TypeScript/Baileys, SQLite | [GitHub](https://github.com/jlucaso1/whatsapp-mcp-ts) |
| `Whatsapp-MCP-Server` | Business API | [GitHub](https://github.com/mattcoatsworth/Whatsapp-MCP-Server) |

**MCP recommandé :** `whatsapp-mcp-ts` (stockage SQLite, performant)

**Prérequis :**
- WhatsApp sur smartphone
- Scan QR code pour liaison Web
- Session active maintenue

**Permissions :**
- [x] Lecture (messages, contacts, médias)
- [x] Écriture (envoi messages)
- [ ] Suppression (limité)

⚠️ **Note légale :** L'automatisation WhatsApp personnel peut violer les ToS. Utiliser avec prudence.

---

## Bootstrap (collecte initiale)

**Méthode 1 : Export manuel (recommandé)**
1. Ouvrir conversation WhatsApp
2. Menu ⋮ → Plus → Exporter discussion
3. Choisir "Avec médias" ou "Sans médias"
4. Envoyer vers email ou stockage
5. Extraire dans `DATA/PENDING/whatsapp/`

**Méthode 2 : Via MCP**
```bash
# Configurer whatsapp-mcp-ts
{
  "mcpServers": {
    "whatsapp": {
      "command": "npx",
      "args": ["-y", "@jlucaso1/whatsapp-mcp-ts"]
    }
  }
}
# Scanner le QR code au premier lancement
```

**Méthode 3 : Base de données locale (Android)**
```bash
# Base WhatsApp (backup non chiffré)
adb pull /sdcard/WhatsApp/Databases/msgstore.db
# Nécessite root ou backup ADB
```

**Période recommandée :** Conversations importantes, 1-2 ans

**Destination :** `DATA/PENDING/whatsapp/`

---

## Format des fichiers

**Structure :**
```
whatsapp/
├── index.md                    # Index des conversations
├── contacts/
│   ├── Jean-Dupont.md          # Conversation 1-1
│   └── ...
├── groups/
│   ├── Famille.md
│   ├── Projet-X.md
│   └── ...
└── media/
    ├── images/
    ├── videos/
    ├── audio/
    └── documents/
```

**Format conversation (export natif parsé) :**
```markdown
---
type: chat
contact: Jean Dupont
phone: +33612345678
export_date: 2024-07-15
message_count: 1234
media_count: 56
period:
  start: 2023-01-15
  end: 2024-07-15
---

# Conversation avec [[Jean Dupont]]

## Statistiques
- **Messages :** 1234
- **Médias :** 56
- **Période :** 2023-01-15 → 2024-07-15

---

## Messages importants

### 2024-07-15
> Voici le document final pour le projet.
> — Jean Dupont, 14:32

📎 [[media/documents/Projet_Final.pdf]]

### 2024-07-10
> On confirme le RDV de mardi 10h ?
> — Moi, 09:15

> Parfait, c'est noté !
> — Jean Dupont, 09:18

---

## Médias
- [[media/images/IMG-20240715-001.jpg]]
- [[media/documents/Contrat.pdf]]
```

**Format groupe :**
```markdown
---
type: group
name: Projet X
participants:
  - Jean Dupont
  - Marie Martin
  - Pierre Durand
created: 2024-01-15
message_count: 5678
---

# Groupe : Projet X

**Participants :** 
- [[Jean Dupont]]
- [[Marie Martin]]  
- [[Pierre Durand]]

## Contexte
[Description du groupe, projet associé]

## Messages clés
[Messages importants extraits]
```

---

## Sync incrémentale

**Fréquence :** hebdomadaire ou manuel

**Via MCP (si configuré) :**
- Récupère nouveaux messages depuis dernière sync
- Stocke dans SQLite local
- Export vers fichiers MD

**Via export manuel :**
- Exporter périodiquement les conversations actives
- Parser et merger avec archives existantes

**Critères :**
- Messages reçus depuis dernière sync
- Nouveaux médias
- Nouvelles conversations

---

## Actions disponibles (via MCP)

**Lecture :**
- `get_chats` — Lister conversations
- `get_messages` — Messages d'une conversation
- `search_messages` — Recherche full-text
- `get_contacts` — Liste contacts

**Écriture :**
- `send_message` — Envoyer message texte
- `send_media` — Envoyer fichier/image
- `send_location` — Envoyer position

---

## Parsing export WhatsApp

**Format export natif :**
```
15/07/2024, 14:32 - Jean Dupont: Message texte
15/07/2024, 14:33 - Jean Dupont: <Media omis>
15/07/2024, 14:35 - Vous: Réponse
```

**Script de parsing :**
```python
import re
from datetime import datetime

pattern = r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.+)'

with open('_chat.txt', 'r') as f:
    for line in f:
        match = re.match(pattern, line)
        if match:
            date, sender, message = match.groups()
            # Traiter le message
```

---

## Liens et relations

- Contact → [[People/Nom]]
- Groupe projet → [[NOW/Projet]]
- Médias → `_whatsapp/media/`
- Références → [[emails/...]], [[meetings/...]]

---

## Notes

**Limites légales :**
- WhatsApp interdit l'automatisation non-officielle
- Risque de ban du compte
- Business API = seule option légale pour entreprises

**Alternatives officielles :**
- **WhatsApp Business API** : pour entreprises, payant
- **WhatsApp Business App** : gratuit, fonctions limitées

**Sécurité :**
- Les exports contiennent données sensibles
- Chiffrer les archives
- Ne pas stocker en cloud public

**Médias :**
- Images/vidéos volumineuses → compresser ou lier
- Documents → extraire contenu si possible
- Audio → transcrire si important

**Bonnes pratiques :**
- Export manuel = plus sûr et légal
- Archiver les conversations clés seulement
- Anonymiser si partage

_Les configurations spécifiques (conversations à surveiller) sont dans `local/TOOLS.md`._
