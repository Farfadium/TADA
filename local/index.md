# local

> Configuration et logs spécifiques à cette instance TADA.

## Contenu

| Fichier/Dossier | Description |
|-----------------|-------------|
| [TOOLS.md](TOOLS.md) | Configuration sources actives (email, calendar, meetings, etc.) |
| [logs.md](logs.md) | Journal des actions système (décisions utilisateur, actions significatives) |
| [logs_routines.md](logs_routines.md) | Journal d'exécution des routines |
| [analyse-logs.md](analyse-logs.md) | Rapport d'analyse des conversations (priorités, frustrations, améliorations) |
| [Claude_logs/](Claude_logs/) | Transcripts des conversations (JSONL) |

## Principe

Ce dossier contient **uniquement** les données spécifiques à cette instance :
- Configuration des sources (comptes, MCP, statut)
- Logs d'exécution
- Décisions utilisateur
- Transcripts des conversations

Le contenu de `_SYSTEM/` (hors `local/`) est agnostique et réutilisable sur n'importe quelle instance TADA.
