---
description: Configuration source Telegram — sync messages, channels, groupes vers TADA
---

# Telegram

> Messagerie cloud — chats, groupes, channels, bots.

**Type :** `messaging`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Bot API + MTProto pour users)
- [x] MCP disponible (plusieurs options)
- [x] Export manuel (Telegram Desktop → Export)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `mcp-telegram` (sparfenyuk) | MTProto complet | [GitHub](https://github.com/sparfenyuk/mcp-telegram) |
| `telegram-mcp` (chigwell) | Telethon, complet | [GitHub](https://github.com/chigwell/telegram-mcp) |
| `telegram-mcp` (chaindead) | NPM, dialogs/messages | [GitHub](https://github.com/chaindead/telegram-mcp) |
| `mcp-telegram` (dryeab) | MCP Server basique | [GitHub](https://github.com/dryeab/mcp-telegram) |

**MCP recommandé :** `telegram-mcp` (chaindead) — NPM, bien documenté

**Credentials nécessaires :**
- Pour **Bot API** : Bot Token via @BotFather
- Pour **MTProto/User** : 
  - API ID et API Hash : https://my.telegram.org
  - Session auth (code SMS)

**Permissions :**
- [x] Lecture (messages, contacts, médias)
- [x] Écriture (envoi messages)
- [ ] Suppression (possible mais attention)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Export Telegram Desktop (recommandé)**
1. Telegram Desktop → Settings → Advanced → Export
2. Sélectionner les chats à exporter
3. Format JSON ou HTML
4. Extraire dans `DATA/PENDING/telegram/`

**Méthode 2 : Via MCP MTProto**
```bash
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "xxx",
        "TG_API_HASH": "xxx"
      }
    }
  }
}
# Première connexion : auth par code SMS
```

**Méthode 3 : Bot API (limité aux interactions avec le bot)**
```bash
# Récupérer les updates du bot
curl "https://api.telegram.org/bot$TOKEN/getUpdates"
```

**Période recommandée :** Conversations importantes, 1-2 ans

**Destination :** `DATA/PENDING/telegram/`

---

## Format des fichiers

**Structure :**
```
telegram/
├── index.md
├── contacts/
│   ├── Jean-Dupont.md
│   └── ...
├── groups/
│   ├── Groupe-1.md
│   └── ...
├── channels/
│   └── Channel-1.md
└── media/
    └── ...
```

**Format conversation :**
```markdown
---
type: private_chat
user_id: 123456789
username: jeandupont
first_name: Jean
last_name: Dupont
phone: +33612345678
message_count: 1500
---

# Conversation avec [[Jean Dupont]]

**Username :** @jeandupont
**Téléphone :** +33 6 12 34 56 78

## Messages importants

### 2024-07-15
> Message important
> — Jean Dupont, 14:32

### 2024-07-10
> Document partagé
> — Moi, 09:15
> 📎 [[media/document.pdf]]
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via MTProto (MCP) :**
```python
# Récupérer messages depuis une date
messages = await client.get_messages(
    chat_id,
    offset_date=last_sync_date,
    limit=100
)
```

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (Bot API webhooks)
- [x] Polling API (getUpdates ou MTProto)
- [ ] Sync manuelle uniquement

**Webhooks Bot API :**
```bash
# Configurer webhook
curl "https://api.telegram.org/bot$TOKEN/setWebhook" \
  -d "url=https://your-domain.com/webhook/telegram"

# Réception
POST /webhook/telegram
{
  "update_id": 123,
  "message": {
    "message_id": 456,
    "from": {"id": 789, "first_name": "Jean"},
    "chat": {"id": 789, "type": "private"},
    "text": "Hello"
  }
}
```

**Long polling Bot API :**
```bash
# Attendre les updates (timeout 30s)
curl "https://api.telegram.org/bot$TOKEN/getUpdates?timeout=30&offset=$LAST_UPDATE_ID"
```

**MTProto (temps réel) :**
```python
# Telethon gère les updates en temps réel
@client.on(events.NewMessage)
async def handler(event):
    print('New message:', event.message.text)
```

**Events disponibles (Bot API) :**
- `message` — Nouveau message
- `edited_message` — Message édité
- `channel_post` — Post dans un channel
- `callback_query` — Bouton inline cliqué
- `inline_query` — Query inline

**Setup requis :**
1. **Bot API** : Créer bot via @BotFather
2. **MTProto** : API ID/Hash sur my.telegram.org
3. Endpoint HTTPS pour webhooks
4. Ou connexion persistante pour MTProto

**Fréquence recommandée :**
- Webhooks/MTProto : temps réel
- Long polling : quasi temps réel
- Polling classique : toutes les 1-5 minutes

---

## Actions disponibles (via MCP)

**Lecture :**
- `get_dialogs` — Lister conversations
- `get_messages` — Messages d'un chat
- `get_contacts` — Liste contacts
- `search_messages` — Recherche

**Écriture :**
- `send_message` — Envoyer message
- `send_file` — Envoyer fichier
- `forward_message` — Transférer

---

## Mapping Telegram → TADA

| Telegram | TADA |
|----------|------|
| Private chat | [[People/Nom]] |
| Group | Groupe ou projet |
| Channel | Source d'info |
| Contact | [[People/Nom]] |
| Media | `_telegram/media/` |

---

## Notes

**Bot API vs MTProto :**
- Bot API : Simple, limité aux interactions bot
- MTProto : Complet, accès compte user

**Export Desktop :**
- Meilleur pour backup complet
- Format JSON structuré
- Inclut tous les médias

**Limites Bot API :**
- 30 messages/seconde
- Fichiers jusqu'à 50 MB (bots)
- Pas d'accès historique complet

**Sécurité :**
- Sessions MTProto = accès total au compte
- Ne jamais partager API hash/sessions
- Utiliser 2FA

_Les configurations spécifiques sont dans `local/TOOLS.md`._
