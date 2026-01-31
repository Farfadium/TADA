---
A quoi sert ce fichier:
Checklist proactive — Liste des vérifications périodiques (emails urgents, INBOX, projets incomplets) et règles de notification
---

# HEARTBEAT.md — Checklist proactive

Ce fichier est lu à chaque heartbeat (check périodique). Garde-le court.

## Checks à effectuer

- [ ] **Emails** — Messages urgents non lus ?
- [ ] **INBOX** — Fichiers en attente de décision ?
- [ ] **Projets incomplets** — Scan DATA/NOW/*/index.md pour sections vides
- [ ] **RDV du jour** — Rappeler les meetings/deadlines du jour
- [ ] **Actions urgentes** — Scanner les "À faire" des projets actifs

## Derniers checks

| Check | Dernier | Résultat |
|-------|---------|----------|
| Emails | — | — |
| INBOX | — | — |

## Règles

**Parler quand :**
- Email important arrivé
- Fichier INBOX > 7 jours
- Ça fait > 8h sans contact

**Se taire (`HEARTBEAT_OK`) quand :**
- Nuit (23h-8h) sauf urgence
- Rien de nouveau depuis le dernier check
- Check fait il y a < 30 min

## Travail de fond autorisé

Sans demander :
- Lire et organiser les fichiers mémoire
- Vérifier l'état des projets (git status, etc.)
- Mettre à jour la documentation
- Commit et push les changements
