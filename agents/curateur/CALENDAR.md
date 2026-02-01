---
A quoi sert ce fichier:
Convention Calendrier — Hub quotidien centralisant events, meetings, conversations avec liens vers sources et projets
---

# Calendrier — Journal d'activité

> Un fichier par jour qui centralise tout ce qui s'est passé.

## Concept

Le calendrier est une **troisième référence centrale** (avec Annuaires et Tâches) :

| Référence | Question | Format |
|-----------|----------|--------|
| Annuaires (People/, Orgs/) | Qui ? | 1 fiche par entité |
| TASKS-INDEX.md | Quoi faire ? | Index + tâches dans projets |
| **Calendrier** | Quand ? Qu'est-ce qui s'est passé ? | 1 fichier par jour |

## Structure

```
DATA/calendar/
├── index.md           # Vue d'ensemble, navigation
├── 2026/
│   ├── 01/
│   │   ├── 2026-01-30.md
│   │   └── 2026-01-31.md
│   └── 02/
└── 2025/
    └── ...
```

## Format d'un fichier jour

```markdown
# YYYY-MM-DD

## Meetings
- HH:MM Titre du meeting → [[NOW/Projet/]]
  - 🎙️ [[fireflies/YYYY-MM-DD_Titre.md]]
  - 📋 [[miro/Board_Associé]] (si applicable)

## Conversations
- 💬 Canal : résumé court → [[projet lié si pertinent]]

## Emails importants
- 📧 Sujet email → [[projet lié]]
  - 📎 [[attachments/YYYY/fichier.pdf]] (si PJ)

## Notes
(Notes libres du jour)
```

## Principe clé : le calendrier est un INDEX

**Les fichiers sources restent où ils sont** :
- Fireflies → `DATA/fireflies/` ou `ARCHIVE/Meetings/`
- Miro → `DATA/miro/` ou `ARCHIVE/Boards/`
- Emails → dans les projets ou `ARCHIVE/Emails/`

**Le calendrier fait les liens**, il ne duplique pas le contenu.

## Lien bidirectionnel

### Dans le calendrier → vers les projets
```markdown
- 14:00 Call Thibaut → [[NOW/Sidekicks/Coaching/Thibaut]]
```

### Dans les projets/fiches → vers le calendrier
```markdown
## Historique rencontres
| Date | Contexte | Lien |
|------|----------|------|
| 2026-01-31 | Call suivi | [[calendar/2026/01/2026-01-31]] |
| 2026-01-15 | Première session | [[calendar/2026/01/2026-01-15]] |
```

## Génération

Le calendrier peut être :
1. **Généré automatiquement** à partir des events calendar importés
2. **Enrichi manuellement** avec conversations, notes
3. **Mis à jour par le Curateur** lors du tri de PENDING/

## Traitement des 42K events calendar

Les fichiers individuels dans `PENDING/calendar/` sont **consolidés** :
1. Lire tous les events d'une journée
2. Créer/mettre à jour le fichier `calendar/YYYY/MM/YYYY-MM-DD.md`
3. Ajouter les liens vers projets si identifiables
4. Supprimer les fichiers individuels après consolidation

**Events sans intérêt** (récurrents vides, annulés) : ne pas inclure ou marquer comme mineurs.

## Icônes standard

| Icône | Signification |
|-------|---------------|
| 🎙️ | Transcript Fireflies |
| 📋 | Board Miro |
| 📧 | Email |
| 📎 | Pièce jointe |
| 💬 | Conversation (Telegram, etc.) |
| 📞 | Appel téléphonique |
| 🏠 | Event personnel/famille |

---

*Ce document définit la convention. Le Curateur l'applique lors du tri.*
