# scripts

> Scripts de maintenance du système TADA.

## Contenu

| Script | Description |
|--------|-------------|
| [build-claude-md.sh](build-claude-md.sh) | Régénère `CLAUDE.md` à partir des fichiers `_SYSTEM/` |

## Utilisation

Les scripts sont exécutés par l'IA après modification des fichiers sources dans `_SYSTEM/`.

**Exemple :**
Après modification de `_SYSTEM/2-Automate/routines.md`, l'IA exécute `build-claude-md.sh` pour mettre à jour `CLAUDE.md`.
