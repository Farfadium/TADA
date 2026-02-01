# Slack — Source

## Config

```yaml
api: Slack API (à configurer)
auth: OAuth token (à obtenir)
status: ⏳ Non connecté
```

## Filtres

```yaml
workspaces:
  - name: Sidekicks
    channels_inclus:
      - general
      - important
      - sales
    channels_exclus:
      - random
      - bots
    dms: contacts connus uniquement
    
  - name: Evaneos
    channels_inclus:
      - board
      - founders
    channels_exclus:
      - random

periode:
  debut: 2024-01-01
  fin: now

exclure:
  - messages de bots (sauf résumés)
  - reactions seules
  - threads < 3 messages
```

## Status

| Métrique | Valeur |
|----------|--------|
| Dernière sync | — |
| Messages collectés | 0 |

## Issues

- 🔴 Non connecté — auth à configurer
