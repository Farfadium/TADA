---
A quoi sert ce fichier:
Journal des actions du système — Log des routines exécutées, décisions utilisateur (pour adapter comportement), actions significatives par date
---

# Logs

> Journal des actions, routines et décisions.

---

## Routines

| Date | Routine | Résultat | Notes |
|------|---------|----------|-------|
| 2026-01-26 | init-système | partiel | Structure créée, pas de projets |

---

## Décisions utilisateur

| Date | Proposition | Réponse | Action |
|------|-------------|---------|--------|
| _exemple_ | Connecter WhatsApp ? | non | Ne plus proposer pendant 30j |

---

## Actions

### 2026-01-27

- Règle ajoutée : enrichissement fiches People (recherche web + photos)
- Règle ajoutée : documents partagés (ARCHIVE/Administratif/, liens depuis projets)
- Configuration Google Calendar MCP (yvan@evaneos.com)
- Création projet Les Jaunets + 15 fiches People + 1 fiche Entreprise
- Téléchargement PJ emails : Protocole V3, Consultation FIDAL, Avis imposition
- Photos récupérées : Adeline Pithois-Guillou, Anthony Melet
- Évolution TADA : Trust/Automate/Document/Act
  - T: Lisible + Personnalisé
  - A: Inbox + Maintenance
  - D: Index + Liens
  - A: Instantané + Proactif
- Restructuration sources de capture (agnostique)
  - Template générique `sources/_template.md`
  - Sources : email.md, messaging.md, calendar.md, files.md
  - Configuration instance dans `local/TOOLS.md`
- Création système de logs structuré (routines + décisions + actions)
- Création routine sync (démarrage session)
- Création section 4-Act/ (Instantané + Proactif)
- Suppression 4-Adapt/ (remplacé par 4-Act/)
- Suppression 1-Trust/sources/ (déplacé vers 2-Automate/sources/)

### 2026-01-26

- Création de la structure TADA (_SYSTEM, NOW, GARDEN, ARCHIVE)
- Versionning de claude.md
- Restructuration de CLAUDE.md autour de TADA
- Renommage PROJETS → NOW, PURGATOIRE → PENDING
- Création de _SYSTEM/local/ pour les données personnelles
