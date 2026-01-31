# DATA-COLLECTION.md — Collecte et traitement des données sources

**Objectif** : Définir comment récupérer, stocker et préparer les données brutes avant le tri TADA.

---

## Sources de données

| Source | Outil | Données |
|--------|-------|---------|
| **Gmail** | `gog gmail` | Emails + pièces jointes |
| **Google Calendar** | `gog calendar` | Events passés et futurs |
| **Folk CRM** | API Folk | Contacts + groupes |
| **Fireflies** | API Fireflies | Transcripts meetings |
| **Miro** | API Miro | Boards (liens + métadonnées) |

---

## Destination

Tout va dans `DATA/PENDING/` en attente de tri :

```
DATA/PENDING/
├── emails/
│   └── [YYYY/]
│       └── YYYY-MM-DD_Expediteur_Sujet.md
├── attachments/
│   └── [YYYY/]
│       ├── fichier.pdf
│       └── fichier.pdf.md      # Companion
├── calendar/
│   └── YYYY-MM-DD_Titre.md
├── fireflies/
│   └── YYYY-MM-DD_Titre.md
├── folk/
│   ├── people/
│   └── groups/
├── miro/
│   └── index.md
└── [autres sources]/
```

---

## Règles par source

### 📧 Emails

**Récupération** :
```bash
gog gmail search 'newer_than:18m -category:promotions -category:social' --max 1000
gog gmail get MESSAGE_ID --account yvan.wibaux@gmail.com
```

**Format fichier** :
```markdown
---
id: MESSAGE_ID
thread_id: THREAD_ID
date: YYYY-MM-DD
from: Expéditeur <email@example.com>
to: destinataires
subject: Sujet
---

[Contenu du message]

## Pièces jointes
- [[attachments/YYYY/fichier.pdf]] (téléchargé)
```

**Règle threads/historique** :
- ❌ NE PAS garder l'historique des messages précédents (citations ">" ou "Le XX/XX, Untel a écrit:")
- ✅ Créer un **lien** vers le message précédent : `Réponse à: [[emails/YYYY/YYYY-MM-DD_Message_Precedent.md]]`
- Ainsi le thread est reconstitué par les liens, sans duplication de contenu

**Exemple** :
```markdown
---
id: abc123
thread_id: xyz789
date: 2026-01-15
from: Jean Dupont
subject: Re: Proposition
reply_to: [[emails/2026/2026-01-14_Marie_Martin_Proposition.md]]
---

Merci pour ta proposition, je suis d'accord.

(historique supprimé — voir message lié ci-dessus)
```

### 📎 Pièces jointes

**Récupération** :
```bash
gog gmail download-attachment MESSAGE_ID ATTACHMENT_ID --out DESTINATION
```

**Organisation** :
- Stockées dans `attachments/YYYY/` (même année que l'email source)
- Nom original conservé
- Si doublon : ajouter suffix `_1`, `_2`

**Fichier .md companion** (OBLIGATOIRE pour chaque attachment) :
```markdown
# nom_fichier.pdf

**Type** : application/pdf
**Taille** : 1.2 MB
**Date email** : 2026-01-15
**Email source** : [[emails/2026/2026-01-15_Expediteur_Sujet.md]]

## Contenu
(Résumé ou extraction du contenu — surtout pour PDFs)

## Contexte
(Pourquoi ce fichier est important, de quoi il parle)
```

**Extraction de contenu** :
- PDFs : utiliser `pdftotext` ou `mutool draw -F txt`
- DOCX : utiliser `pandoc` ou `unzip` + parse XML
- Images : description si pertinent
- XLSX : extraire en CSV ou décrire le contenu

### 📅 Calendar

**Récupération** :
```bash
gog calendar events CALENDAR_ID --from YYYY-MM-DD --to YYYY-MM-DD
```

**Format fichier** :
```markdown
---
id: EVENT_ID
date: YYYY-MM-DD
time: HH:MM - HH:MM
location: Lieu
---

# Titre de l'event

## Participants
- participant@email.com

## Description
(description de l'event)

## Liens
- [[fireflies/YYYY-MM-DD_Meeting.md]] (si transcript existe)
```

### 📞 Fireflies (meetings)

**Récupération** : Via API Fireflies (skill fireflies)

**Format fichier** :
```markdown
---
id: TRANSCRIPT_ID
date: YYYY-MM-DD
duration: XXmin
---

# Titre du meeting

## Participants
- Participant 1
- Participant 2

## Résumé
(summary généré par Fireflies)

## Action items
- [ ] Action 1 (@personne)
- [ ] Action 2 (@personne)

## Transcript
(transcript complet ou lien)
```

### 👥 Folk CRM

**Récupération** : Via API Folk (skill folk)

**Format fichier People** :
```markdown
# Prénom Nom

**Email** : ...
**Téléphone** : ...
**Entreprise** : ...
**Groupes** : groupe1, groupe2

## Notes
(notes du CRM)
```

**Format fichier Groups** :
```markdown
# Nom du groupe

## Membres
- [[people/Prénom_Nom.md]]
- [[people/Autre_Personne.md]]
```

### 🎨 Miro

**Récupération** : Via API Miro (skill miro)

**Format** : Index avec liens vers les boards (pas de téléchargement du contenu)

```markdown
# Miro Boards

## Board 1
- **Créé** : YYYY-MM-DD
- **Modifié** : YYYY-MM-DD
- **Lien** : https://miro.com/app/board/XXX
```

---

## Règles générales

### Nommage des fichiers

```
YYYY-MM-DD_Expediteur_Sujet_Court.md
```

- Underscores pour les espaces
- Pas de caractères spéciaux
- Sujet tronqué si trop long (max 50 chars)

### Liens

Toujours utiliser des **liens relatifs** ou **wiki-links** :
- `[[emails/2026/fichier.md]]`
- `[[attachments/2026/doc.pdf]]`
- `[[people/Prénom_Nom.md]]`

Les liens permettent de :
- Reconstituer les threads email
- Relier attachments à leurs emails
- Connecter meetings aux participants
- Naviguer dans Obsidian

### Déduplication

- Si un fichier existe déjà avec le même contenu → ne pas recréer
- Si même nom mais contenu différent → ajouter suffix date ou numéro

### Métadonnées

Chaque fichier doit avoir un **frontmatter YAML** avec au minimum :
- `id` : identifiant source
- `date` : date du document

---

## Commandes de collecte

### Collecte complète (18 mois)

```bash
# Emails
gog gmail search 'newer_than:18m -category:promotions -category:social -category:updates -category:forums' --max 5000

# Calendar
gog calendar events yvan@evaneos.com --from 2024-07-01 --to 2026-02-01

# Fireflies
# Via skill fireflies

# Folk
# Via skill folk

# Miro  
# Via skill miro
```

### Collecte incrémentale (quotidienne)

```bash
# Nouveaux emails depuis 24h
gog gmail search 'newer_than:1d' --max 100
```

---

## Vérification

Après collecte, vérifier :

- [ ] Tous les emails ont leurs pièces jointes téléchargées
- [ ] Tous les attachments ont un fichier .md companion
- [ ] Les threads sont liés (pas de duplication d'historique)
- [ ] Les participants meetings sont liés vers People/
- [ ] Rapport de collecte généré dans `PENDING/RAPPORT.md`

---

*Ce document définit le processus de collecte. Pour le tri et l'organisation, voir [[METHODOLOGY.md]].*
