---
A quoi sert ce fichier:
Index du dossier _SYSTEM — Vue d'ensemble de la structure du système TADA
---

# _SYSTEM

> Contient tout le fonctionnement de TADA, agnostique et partageable (sauf `local/`)

**Principe de reproductibilité :** Tout ce qui est nécessaire pour recréer TADA à l'identique est documenté ici.
- Scripts, configs, automatisations → documentation obligatoire
- Pas de "modifications fantômes"
- Quelqu'un qui clone `_SYSTEM/` reproduit TADA sans secret caché

## Fichiers d'instructions

**Source de vérité :** `instructions.md`
- Contient toutes les instructions pour l'agent IA
- À lire en priorité à chaque session

**Fichier racine :** `/CLAUDE.md`
- Pointe vers `_SYSTEM/instructions.md`
- Fichier réel (pas de symlink) pour compatibilité Google Drive

**Note :** Pas de symlinks utilisés (incompatibles avec Google Drive).

## Structure

| Fichier/Dossier | Description |
|-----------------|-------------|
| [instructions.md](instructions.md) | Point d'entrée principal pour l'IA |
| [BOOTSTRAP.md](BOOTSTRAP.md) | Guide de première initialisation |
| [tada.md](tada.md) | Vision et principes fondateurs T.A.D.A |
| [1-Trust/](1-Trust/) | Lisibilité, versionning, personnalité (SOUL.md) |
| [2-Automate/](2-Automate/) | Routines, sources, validation, HEARTBEAT |
| [3-Document/](3-Document/) | Index et liens (répertoires de référence) |
| [4-Act/](4-Act/) | Actions instantanées et proactivité |
| [local/](local/) | Configuration et logs spécifiques à cette instance |
| [scripts/](scripts/) | Scripts de maintenance (build-claude-md.sh) |
