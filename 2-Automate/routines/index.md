# Routines

> Détails de chaque routine TADA.

## Templates

| Fichier | Description |
|---------|-------------|
| [_template.md](_template.md) | Template pour créer de nouvelles routines |

## Routines système

| Fichier | Routine | Déclencheur |
|---------|---------|-------------|
| [sync.md](sync.md) | Sync | Session (démarrage) |
| [init-systeme.md](init-systeme.md) | Init système | DATA/NOW/ vide |
| [init-projet.md](init-projet.md) | Init projet | Tag #init |
| [commit.md](commit.md) | Commit | Tag #commit, modifications significatives |
| [ajout-source.md](ajout-source.md) | Ajout source | Tag #source |
| [ajout-regle.md](ajout-regle.md) | Ajout règle | Tag #rule |
| [analyse-logs.md](analyse-logs.md) | Analyse logs | Mensuel, tag #analyse-logs |

## Routines contenu

| Fichier | Routine | Déclencheur |
|---------|---------|-------------|
| [tri-inbox.md](tri-inbox.md) | Tri INBOX | Fichier en INBOX |
| [tri-emails.md](tri-emails.md) | Tri emails | Tag #emails |
| [revue-projets.md](revue-projets.md) | Revue projets | Vendredi, tag #revue |
| [maj-index.md](maj-index.md) | Mise à jour index | Fichier ajouté/supprimé, tag #maj-index |
| [maj-projet.md](maj-projet.md) | Mise à jour projet | Tag #projet |

## Utilisation

Chaque routine a:
- **Déclencheurs** : Temps, Logique ou Tag
- **Actions** : Étapes à exécuter
- **Validation** : Oui/Non
- **Logging** : Tracé dans `local/logs_routines.md`
