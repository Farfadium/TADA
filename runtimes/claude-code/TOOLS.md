# TOOLS.md - Claude Code (Local Mac)

Configuration spécifique pour le runtime Claude Code sur Mac local.

## Environnement

- **OS** : macOS
- **Runtime** : Claude Code CLI
- **Workspace** : ~/tada (sync git avec serveur)

## Outils disponibles

### Natifs
- Système de fichiers local
- Terminal/shell
- Git

### À configurer
- SSH vers serveur Hetzner
- Clés API (voir .env local)

## Notes

Ce runtime n'a pas de heartbeat automatique — il est invoqué à la demande.
Pour les tâches récurrentes, utiliser le runtime Moltbot sur le serveur.
