# CONTRIBUTING — Conventions TADA

## Règles de nommage des fichiers

TADA doit fonctionner sur tous les systèmes (Linux, macOS, Windows, Obsidian, iCloud, etc.). **Les noms de fichiers doivent être 100% portables.**

### ❌ Interdit

| Caractère | Exemple |
|-----------|---------|
| **Espaces** | `Nicolas Doumenc.md` |
| **Accents** | `Rémi`, `Clémentine`, `Crédit` |
| **Apostrophes** | `d'Épargne`, `l'IA` |
| **Caractères spéciaux** | `()`, `«»`, `!`, `?` dans les noms |
| **Entités HTML** | `&#39;` |

### ✅ Correct

| Règle | Exemple |
|-------|---------|
| Tirets `-` au lieu des espaces | `Nicolas-Doumenc.md` |
| Sans accents | `Remi`, `Clementine`, `Credit` |
| Sans apostrophes | `d-Epargne`, `l-IA` |
| Alphanumérique + tirets | `2024-01-15_Meeting-avec-Jerome.md` |

### Conventions spécifiques

| Type | Format |
|------|--------|
| **People** | `Prenom-Nom.md` |
| **Orgs** | `Nom-Organisation.md` |
| **Fireflies** | `YYYY-MM-DD_Titre-du-meeting.md` |
| **Calendar** | `YYYY-MM-DD_Titre-event.md` |
| **Attachments** | `YYYY-MM-DD_Expediteur_Sujet/fichier.ext` |

### Script de nettoyage

En cas de fichiers non conformes, exécuter :
```bash
bash scripts/clean-filenames.sh
```

## Structure _SYSTEM

Les dossiers de `_SYSTEM` suivent une convention numérotée :
- `1-Trust` — Configuration identité/sécurité
- `2-Automate` — Automation, heartbeat, crons
- `3-Document` — Documentation, contributing
- `4-Act` — Actions, workflows

---

*Ces règles sont impératives. Tous les agents (Cassiopée, Collecteur, Curateur, Scribe) doivent les respecter.*
