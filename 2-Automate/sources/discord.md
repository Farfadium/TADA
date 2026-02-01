---
description: Configuration source Discord — sync messages, serveurs, channels vers TADA
---

# Discord

> Plateforme communautaire — serveurs, channels, DMs, voice.

**Type :** `messaging`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Discord Bot API)
- [x] MCP disponible (discord-mcp)
- [x] Export manuel (DiscordChatExporter)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `discord-mcp` (SaseQ) | JDA, complet | [GitHub](https://github.com/SaseQ/discord-mcp) |
| `Discord_MCP_MOD` | LLM interaction | [GitHub](https://github.com/Kaleemullah-Younas/Discord_MCP_MOD) |
| `discord-mcp-server` (ReesavGupta) | Go, robuste | [GitHub](https://github.com/ReesavGupta/discord-mcp-server) |

**MCP recommandé :** `discord-mcp` (SaseQ)

**Credentials nécessaires :**
- Bot Token : https://discord.com/developers/applications
- Ou User Token (non recommandé, ToS)

**Permissions bot requises :**
- `READ_MESSAGE_HISTORY`
- `VIEW_CHANNEL`
- `SEND_MESSAGES` (pour écriture)

**Permissions :**
- [x] Lecture (messages, channels, users)
- [x] Écriture (envoi via bot)
- [ ] Suppression (avec permissions)

---

## Bootstrap (collecte initiale)

**Méthode 1 : DiscordChatExporter (recommandé)**
```bash
# Télécharger: https://github.com/Tyrrrz/DiscordChatExporter

# Export CLI
DiscordChatExporter.Cli export \
  -t $BOT_TOKEN \
  -c $CHANNEL_ID \
  -f Json \
  -o export.json
```

**Méthode 2 : Via MCP**
```bash
{
  "mcpServers": {
    "discord": {
      "command": "npx",
      "args": ["-y", "@saseq/discord-mcp"],
      "env": {
        "DISCORD_TOKEN": "xxx"
      }
    }
  }
}
```

**Méthode 3 : Via API directe**
```bash
# Récupérer messages d'un channel
curl "https://discord.com/api/v10/channels/$CHANNEL_ID/messages?limit=100" \
  -H "Authorization: Bot $TOKEN"
```

**Période recommandée :** Channels importants, 6-12 mois

**Destination :** `DATA/PENDING/discord/`

---

## Format des fichiers

**Structure :**
```
discord/
├── index.md
├── servers/
│   └── Server-Name/
│       ├── index.md
│       └── channels/
│           ├── general.md
│           └── projet-x.md
├── dms/
│   └── Jean-Dupont.md
└── media/
    └── ...
```

**Format channel :**
```markdown
---
id: CHANNEL_ID
name: projet-x
type: text
server: Server Name
server_id: SERVER_ID
topic: "Discussion projet X"
---

# #projet-x

**Serveur :** [[Servers/Server Name]]
**Topic :** Discussion projet X

## Messages importants

### 2024-07-15

> 🎉 Le projet est live !
> — [[Jean#1234]], 16:45
> 👍 5 | 🎉 3

### Thread: Discussion technique
> Détails techniques...
> — [[Marie#5678]], 10:30
```

**Format message :**
```markdown
---
id: MESSAGE_ID
author: Username#1234
author_id: USER_ID
channel: channel-name
timestamp: 2024-07-15T14:32:00Z
edited: false
reactions: [{emoji: "👍", count: 3}]
attachments: []
---

> Contenu du message
> — [[Username#1234]], 14:32
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via API avec after :**
```bash
curl "https://discord.com/api/v10/channels/$CHANNEL_ID/messages?after=$LAST_MESSAGE_ID&limit=100" \
  -H "Authorization: Bot $TOKEN"
```

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (Gateway WebSocket temps réel)
- [x] Polling API (messages endpoint)
- [ ] Sync manuelle uniquement

**Gateway WebSocket (temps réel) :**
```javascript
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

client.on('messageCreate', message => {
  console.log('New message:', message.content);
});

client.login(TOKEN);
```

**Events Gateway disponibles :**
- `MESSAGE_CREATE` — Nouveau message
- `MESSAGE_UPDATE` — Message édité
- `MESSAGE_DELETE` — Message supprimé
- `MESSAGE_REACTION_ADD/REMOVE` — Réactions
- `CHANNEL_CREATE/UPDATE/DELETE` — Channels
- `GUILD_MEMBER_ADD/REMOVE` — Membres

**Discord Webhooks (outgoing) :**
```bash
# Webhook serveur (pour recevoir dans Discord, pas depuis)
# Discord n'a pas de webhooks sortants natifs
# Utiliser le Gateway ou un bot
```

**Polling (alternative) :**
```bash
# Messages récents
curl "https://discord.com/api/v10/channels/$CHANNEL_ID/messages?limit=50" \
  -H "Authorization: Bot $TOKEN"

# Comparer avec dernier message_id stocké
```

**Setup requis :**
1. Créer application sur Discord Developer Portal
2. Créer un bot et récupérer le token
3. Inviter le bot sur les serveurs avec OAuth2
4. Activer les intents nécessaires (Message Content)

**Fréquence recommandée :**
- Gateway WebSocket : temps réel
- Polling : toutes les 1-5 minutes

---

## Actions disponibles (via MCP)

**Lecture :**
- `get_guilds` — Lister serveurs
- `get_channels` — Channels d'un serveur
- `get_messages` — Messages d'un channel
- `search_messages` — Recherche

**Écriture :**
- `send_message` — Envoyer message
- `add_reaction` — Ajouter réaction
- `create_thread` — Créer thread

---

## Mapping Discord → TADA

| Discord | TADA |
|---------|------|
| Server | Organisation ou communauté |
| Channel | Catégorie ou projet |
| Thread | Sous-discussion |
| User | [[People/Username#Disc]] |
| DM | Communication privée |
| Role | Tag ou groupe |

---

## Notes

**Intents requis :**
- `MESSAGE_CONTENT` : Privilégié, demande vérification
- Sans cet intent, pas accès au contenu des messages

**Rate limits :**
- 50 requests/second par bot
- Headers X-RateLimit-* pour tracking

**DiscordChatExporter :**
- Meilleur pour export historique massif
- Support HTML, JSON, CSV, TXT
- Inclut médias et attachments

**Particularités :**
- Les messages sont paginés par ID (snowflake)
- Les threads sont des channels spéciaux
- Les attachments ont des URLs temporaires

**Sécurité :**
- Ne jamais utiliser de user token (ToS violation)
- Bot token = accès limité aux serveurs invités
- Permissions granulaires possibles

_Les configurations spécifiques sont dans `local/TOOLS.md`._
