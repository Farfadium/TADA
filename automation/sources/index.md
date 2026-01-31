# Sources

> Configuration des sources de capture (template agnostique).

## Templates

| Fichier | Description |
|---------|-------------|
| [_template.md](_template.md) | Template pour configurer une nouvelle source |

## Sources disponibles

| Fichier | Source | Type |
|---------|--------|------|
| [email.md](email.md) | Email | Gmail, Outlook, IMAP |
| [calendar.md](calendar.md) | Calendar | Google Calendar, Outlook Calendar |
| [meetings.md](meetings.md) | Meetings | Fireflies, Otter |
| [messaging.md](messaging.md) | Messaging | WhatsApp, Telegram, Slack |
| [files.md](files.md) | Files | Système de fichiers local |
| [folk.md](folk.md) | CRM | Folk API/CSV |
| [miro.md](miro.md) | Collaboration | Miro Board Export API |

## Configuration instance

La configuration spécifique à cette instance (comptes, MCP, statut) est dans `_SYSTEM/local/TOOLS.md`.

## Structure d'une source

Chaque fichier source contient:
- **Configuration** : MCP possibles, accès (lecture/écriture/suppression)
- **Comportement** : Ce que l'IA peut/ne peut pas faire
- **Sync** : Fréquence, critères de récupération
- **Archivage** : Format Markdown, vérification doublons, création fiches People
- **Recherche** : Comment rechercher pour un projet
