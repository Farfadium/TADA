# DATA-COLLECTION.md — Collecte des données sources

**Objectif** : Récupérer toutes les données disponibles et les déposer dans `DATA/PENDING/` pour tri.

---

## Sources disponibles

| Source | Documentation | Données |
|--------|---------------|---------|
| **Email** | [[sources/email.md]] | Emails + pièces jointes |
| **Calendar** | [[sources/calendar.md]] | Events passés et futurs |
| **Folk CRM** | [[sources/folk.md]] | Contacts + groupes |
| **Meetings** | [[sources/meetings.md]] | Transcripts (Fireflies) |
| **Miro** | [[sources/miro.md]] | Boards (liens) |
| **Files** | [[sources/files.md]] | Documents locaux |

Chaque source a sa propre documentation dans `_SYSTEM/2-Automate/sources/`.

---

## Destination

Tout va dans `DATA/PENDING/` :

```
DATA/PENDING/
├── emails/
│   └── [YYYY/]
├── attachments/
│   └── [YYYY/]
├── calendar/
├── fireflies/
├── folk/
│   ├── people/
│   └── groups/
├── miro/
└── [autres]/
```

---

## Processus de collecte

### 1. Collecte initiale (bootstrap)

Récupérer toutes les données sur une période (ex: 18 mois) :

```bash
# Voir chaque source pour les commandes spécifiques
```

### 2. Collecte incrémentale (quotidienne)

Récupérer les nouvelles données depuis la dernière sync.

Fréquence définie par source (voir documentation).

---

## Règles générales

### Nommage des fichiers

```
YYYY-MM-DD_Origine_Sujet_Court.md
```

- Underscores pour les espaces
- Pas de caractères spéciaux
- Sujet tronqué si trop long (max 50 chars)

### Liens

Toujours utiliser des **liens wiki** :
- `[[emails/2026/fichier.md]]`
- `[[attachments/2026/doc.pdf]]`
- `[[People/Prénom_Nom.md]]`

Les liens permettent de :
- Reconstituer les threads
- Relier fichiers à leurs sources
- Naviguer dans Obsidian

### Métadonnées

Chaque fichier doit avoir un **frontmatter YAML** avec au minimum :
- `id` : identifiant source
- `date` : date du document

### Déduplication

- Si fichier identique existe → ne pas recréer
- Si même nom mais contenu différent → ajouter suffix

---

## Vérification post-collecte

- [ ] Toutes les sources ont été récupérées
- [ ] Les pièces jointes sont téléchargées
- [ ] Les fichiers .md companions existent (attachments)
- [ ] Les liens sont en place (threads, sources)
- [ ] Rapport généré : `PENDING/RAPPORT.md`

---

## Liens

- **Tri des données** : [[METHODOLOGY.md]]
- **Structure cible** : [[PROPOSAL-YVAN.md]] (exemple)
- **Sources** : `_SYSTEM/2-Automate/sources/`

---

*Pour les règles spécifiques à chaque source (format, threading, attachments...), voir la documentation de la source concernée.*
