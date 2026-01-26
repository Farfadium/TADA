## Routines

Des actions déclenchées par le temps, la logique, ou un tag.

| Routine | Temps | Logique | Tag |
|---------|-------|---------|-----|
| Tri INBOX | 7j sans tri | Fichier déposé | |
| Tri emails | | | #emails |
| Revue projets | Vendredi | | #revue |
| Alerte PENDING | | Document en attente | |
| Mise à jour index | | Fichier ajouté/supprimé | |
| Log conversation | | Modif CLAUDE.md | #log |
| Mise à jour projet | | | #projet |
| Ajout règle | | | #rule |

**Format tri emails :**
```
**Email X/Y** — Expéditeur | Sujet | date relative

> Contenu (si court)

**Actions :**
- Label : ...
- PJ : ... (si PJ à stocker)
- Gmail : ... (archiver, répondre...)
- TADA : ... (mettre à jour projet...)
```
