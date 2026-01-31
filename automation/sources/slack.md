---
description: Configuration source Slack — sync messages, channels, DMs, fichiers vers TADA
---

# Slack

> Messagerie d'équipe — channels, DMs, threads, intégrations.

**Type :** `messaging`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [x] API officielle (Slack Web API)
- [x] MCP disponible (plusieurs options)
- [x] Export manuel (Workspace Export)
- [ ] Scraping/autre

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `slack-mcp-server` (korotovsky) | Complet, GovSlack, Apps | [GitHub](https://github.com/korotovsky/slack-mcp-server) |
| `slack-mcp-server` (AVIMBU) | Basique, bien documenté | [GitHub](https://github.com/AVIMBU/slack-mcp-server) |
| `slack-mcp-server` (piekstra) | Block Kit support | [GitHub](https://github.com/piekstra/slack-mcp-server) |
| `slack-mcp-server` (zencoderai) | Intégration workspaces | [GitHub](https://github.com/zencoderai/slack-mcp-server) |

**MCP recommandé :** `slack-mcp-server` (korotovsky) — le plus complet

**Credentials nécessaires :**
- Slack App avec Bot Token (`xoxb-...`)
- Ou User Token (`xoxp-...`) pour accès personnel
- OAuth scopes requis selon les actions

**Scopes recommandés :**
```
channels:history, channels:read
groups:history, groups:read  
im:history, im:read
mpim:history, mpim:read
users:read, users:read.email
files:read
```

**Permissions :**
- [x] Lecture (messages, channels, users)
- [x] Écriture (post messages)
- [ ] Suppression (admin uniquement)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via MCP**
```bash
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@korotovsky/slack-mcp-server"],
      "env": {
        "SLACK_TOKEN": "xoxb-xxx-xxx-xxx"
      }
    }
  }
}
```

**Méthode 2 : Export Workspace (Admin)**
1. Slack Admin → Settings → Import/Export
2. Export Workspace (Standard = public, Corporate = tout)
3. Télécharger ZIP
4. Extraire dans `DATA/PENDING/slack/`

**Méthode 3 : Via API**
```bash
# Lister les channels
curl -X GET "https://slack.com/api/conversations.list" \
  -H "Authorization: Bearer $SLACK_TOKEN"

# Récupérer l'historique
curl -X GET "https://slack.com/api/conversations.history?channel=C1234567" \
  -H "Authorization: Bearer $SLACK_TOKEN"
```

**Période recommandée :** 1 an ou selon plan (Free = 90 jours)

**Destination :** `DATA/PENDING/slack/`

---

## Format des fichiers

**Structure :**
```
slack/
├── index.md                    # Index du workspace
├── channels/
│   ├── general.md
│   ├── projet-x.md
│   └── ...
├── dms/
│   ├── Jean-Dupont.md
│   └── ...
├── threads/
│   └── important-thread-ts.md
└── files/
    └── ...
```

**Format channel :**
```markdown
---
id: C1234567890
name: projet-x
type: channel
is_private: false
created: 2024-01-15
creator: U1234567890
topic: "Discussion projet X"
purpose: "Coordination équipe projet"
members_count: 12
---

# #projet-x

**Type :** Channel public
**Créé :** 2024-01-15 par [[Jean Dupont]]
**Topic :** Discussion projet X
**Membres :** 12

## Contexte
[Description du channel, projet associé]

## Messages importants

### 2024-07-15

> 🎉 Le projet est livré ! Bravo à tous.
> — [[Marie Martin]], 16:45
> 👍 5 | 🎉 3

### 2024-07-10

> Voici le planning final : [lien]
> — [[Pierre Durand]], 10:30
> 📎 [[files/planning-final.pdf]]
```

**Format message :**
```markdown
---
ts: "1720022700.123456"
channel: C1234567890
user: U1234567890
type: message
thread_ts: "1720022600.000000"
reply_count: 5
reactions:
  - name: "+1"
    count: 3
---

> Message texte avec @mention et #channel
> — [[Prénom Nom]], 2024-07-15 14:32

**Thread :** 5 réponses
**Réactions :** 👍 3
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via API :**
```bash
# Messages depuis timestamp
curl -X GET "https://slack.com/api/conversations.history?channel=C123&oldest=1720000000" \
  -H "Authorization: Bearer $SLACK_TOKEN"
```

**Critères :**
- Messages depuis dernier `ts` synchronisé
- Nouveaux channels rejoints
- Fichiers partagés

---

## Actions disponibles (via MCP)

**Lecture :**
- `list_channels` — Lister channels
- `get_channel_history` — Historique messages
- `get_thread_replies` — Réponses thread
- `search_messages` — Recherche full-text
- `get_user_info` — Infos utilisateur
- `list_files` — Fichiers partagés

**Écriture :**
- `post_message` — Poster un message
- `reply_to_thread` — Répondre dans thread
- `add_reaction` — Ajouter emoji
- `upload_file` — Partager fichier

---

## Mapping Slack → TADA

| Slack | TADA |
|-------|------|
| Channel projet | `DATA/NOW/[Projet]/_slack/` |
| DM | `DATA/ARCHIVE/Communications/` |
| User | [[People/Nom]] |
| Fichier | `_slack/files/` |

---

## Workflow recommandé

**Archivage sélectif :**
1. Identifier channels/threads importants
2. Exporter les décisions et informations clés
3. Lier aux fiches People et Projects

**Ce qu'il faut archiver :**
- Décisions importantes
- Annonces et jalons
- Documents partagés
- Threads de décision

**Ce qu'on peut ignorer :**
- Bavardages quotidiens
- Messages éphémères
- GIFs et réactions sans contenu

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (Events API ou Socket Mode)
- [x] Polling API (conversations.history)
- [ ] Sync manuelle uniquement

**Socket Mode (recommandé pour dev/local) :**
```javascript
// Pas besoin d'URL publique
const { App } = require('@slack/bolt');
const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN
});

app.message(async ({ message, say }) => {
  console.log('New message:', message);
});
```

**Events API (webhooks HTTP) :**
```bash
# Configuration dans Slack App Dashboard
# Request URL: https://your-domain.com/slack/events

# Vérification challenge
POST /slack/events
{
  "type": "url_verification",
  "challenge": "xxx"
}
# Répondre avec le challenge

# Réception événement
{
  "type": "event_callback",
  "event": {
    "type": "message",
    "channel": "C1234",
    "user": "U1234",
    "text": "Hello"
  }
}
```

**Events disponibles :**
- `message` — Nouveau message dans un channel
- `message.channels` / `message.groups` / `message.im`
- `reaction_added` / `reaction_removed`
- `file_shared` — Fichier partagé
- `member_joined_channel` / `member_left_channel`
- `channel_created` / `channel_archive`

**Polling (alternative) :**
```bash
# Messages depuis timestamp
curl -X GET "https://slack.com/api/conversations.history?channel=C123&oldest=$LAST_TS" \
  -H "Authorization: Bearer $SLACK_TOKEN"
```

**Setup requis :**
1. Créer Slack App sur api.slack.com
2. Activer Events API ou Socket Mode
3. Souscrire aux événements voulus
4. Installer l'app dans le workspace

**Fréquence recommandée :**
- Socket Mode / Events API : temps réel
- Polling : toutes les 1-5 minutes

---

## Liens et relations

- User → [[People/Nom]]
- Channel projet → [[NOW/Projet]]
- Fichiers → `_slack/files/`
- Mentions → Liens vers fiches

---

## Notes

**Limites API :**
- Rate limits : ~50 req/min selon endpoint
- Free plan : 90 jours d'historique seulement
- Fichiers : URLs temporaires (expiration)

**Export Workspace :**
- Standard : channels publics seulement
- Corporate Export : tout (DMs inclus)
- Nécessite plan Business+ pour Corporate

**Particularités :**
- `ts` (timestamp) = ID unique du message
- `thread_ts` = parent du thread
- Reactions stockées par message

**Sécurité :**
- User tokens = accès personnel, plus large
- Bot tokens = accès limité à ce qui est partagé
- Préférer Bot token pour automatisation

**Bonnes pratiques :**
- Archiver par projet/channel pertinent
- Extraire les décisions des threads longs
- Télécharger les fichiers importants (URLs expirent)

_Les configurations spécifiques (token, channels à surveiller) sont dans `local/TOOLS.md`._
