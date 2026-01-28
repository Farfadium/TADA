### Initialisation projet

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Tag | #init [nom du projet] |

**Impact :** Contenu, Externe

**Contexte :**
Créer la structure complète d'un nouveau projet pour qu'il soit immédiatement opérationnel dans TADA, avec tout le contexte existant récupéré des sources.

**Actions :**

1. Demander les informations de base :
   - Nom du projet
   - Description courte
   - Objectif principal
   - Parties prenantes (personnes, entreprises)

2. Créer la structure de dossiers :
   ```
   DATA/NOW/[Nom Projet]/
   ├── index.md
   ├── _attachments/      # Pièces jointes des emails
   ├── _emails/           # Emails sauvegardés en markdown
   └── _transcripts/      # Transcripts meetings Fireflies
   ```

3. Identifier les mots-clés de routage :
   - Noms des parties prenantes
   - Nom du projet et variantes
   - Domaines email (@exemple.com)
   - Codes ou références spécifiques

4. Configurer Gmail :
   - Créer le label correspondant au projet
   - Proposer un filtre si pertinent

5. **Créer TOUTES les fiches des parties prenantes :**
   - Vérifier si les personnes/entreprises existent dans les répertoires (Glob avant création)
   - **Créer systématiquement les fiches manquantes** — même avec infos minimales
   - Enrichir les fiches avec recherche web si possible
   - Ajouter les liens `[[Nom]]` dans l'index du projet

6. **Récupérer et sauvegarder les emails :**
   - Rechercher tous les emails liés (mots-clés, contacts, domaines)
   - Pour chaque email pertinent :
     - Créer `_emails/YYYY-MM-DD_Expediteur_Sujet.md`
     - Inclure : contenu, réponses, liens vers documents
   - **Télécharger les pièces jointes** (attachments Gmail) dans `_attachments/`
   - **Télécharger les documents liés** (liens dans le corps de l'email) :
     - PDF accessibles directement → télécharger via curl
     - **Google Docs/Slides/Sheets → exporter en PDF** via URL d'export :
       - Slides : `https://docs.google.com/presentation/d/{ID}/export/pdf`
       - Docs : `https://docs.google.com/document/d/{ID}/export?format=pdf`
       - Sheets : `https://docs.google.com/spreadsheets/d/{ID}/export?format=pdf`
     - Nextcloud/Dropbox/etc. → tenter le téléchargement, noter si non accessible
   - Convention : `YYYY-MM-DD_Nom_fichier.ext` ou `YYYY_Nom_document.ext` pour les rapports annuels

7. **Récupérer et sauvegarder les meetings (Fireflies) :**
   - Rechercher les transcripts avec les parties prenantes
   - Pour chaque meeting :
     - Créer `_transcripts/YYYY-MM-DD_Titre.md`
     - Inclure : résumé, points clés, actions, notes détaillées
     - Lien vers Fireflies pour le transcript complet

8. **Récupérer les événements calendrier :**
   - Événements passés → ajouter dans l'historique
   - Événements futurs → ajouter dans "À faire"

9. **Consolider l'index du projet :**
   - Historique chronologique complet
   - Contexte détaillé (issu des meetings/emails)
   - Structure des dossiers avec tous les fichiers
   - Tableaux : pièces jointes, emails, transcripts
   - Questions ouvertes identifiées
   - Prochaines étapes

**Convention de nommage des fichiers :**

| Type | Format | Exemple |
|------|--------|---------|
| Pièce jointe | `YYYY-MM-DD_Nom_Fichier.ext` | `2026-01-05_Interview_Parents.docx` |
| Email | `YYYY-MM-DD_Expediteur_Sujet-court.md` | `2026-01-10_Karen_Elements-Declic.md` |
| Transcript | `YYYY-MM-DD_Titre-meeting.md` | `2026-01-19_Session1_Karen-Yvan.md` |

**Template email sauvegardé :**
```markdown
# Email : [Sujet]

**Date :** [Date]
**De :** [[Nom]] <email>
**À :** email
**Thread ID :** [ID Gmail]

---

## Contenu
[Corps de l'email]

---

## Réponses
**[Date] - [Nom] :** [Contenu de la réponse]

---

## Pièces jointes (attachments Gmail)
| Fichier | Taille | Sauvegardé |
|---------|--------|------------|
| [nom.ext] | X KB | [lien local](../_attachments/...) |

## Documents téléchargés (liens dans l'email)
| Document | Type | Sauvegardé |
|----------|------|------------|
| [Nom du doc] | PDF | [lien local](../_attachments/...) |

## Documents non accessibles
| Document | Type | Statut |
|----------|------|--------|
| [Nom] | Nextcloud | Non accessible (raison) |
```

**Template transcript sauvegardé :**
```markdown
# Meeting [Titre]

**Date :** [Date], [Heure] ([Durée])
**Participants :** [[Personne 1]], [[Personne 2]]
**Lien Fireflies :** [URL]

---

## Résumé
[Short summary]

---

## Points clés
- Point 1
- Point 2

---

## Mots-clés
[Keywords]

---

## Actions identifiées

### [Personne]
- Action 1
- Action 2

---

## Notes détaillées
[Notes complètes du meeting]
```

**Validation requise :** Oui (à chaque étape)

**Exemple :**
```
#init Achat Maison Bordeaux

→ Structure créée :
NOW/Achat Maison Bordeaux/
├── index.md
├── _attachments/
│   ├── 2026-01-15_Compromis_v1.pdf
│   ├── 2026-01-20_Plan_maison.pdf
│   └── 2025_Diagnostic-energetique.pdf  ← téléchargé depuis lien dans email
├── _emails/
│   ├── 2026-01-10_Notaire_Compromis.md
│   └── 2026-01-15_Agence_Visite.md
└── _transcripts/
    └── 2026-01-12_RDV-Banque.md

→ Fiches créées :
- [[Maître Dupont]] (notaire) ✓
- [[ImmoPlus]] (agence) ✓
- [[CréditNord]] (banque) — existait

→ Gmail :
- Label créé : "Achat Maison Bordeaux"

→ Récupéré :
- 4 emails
- 3 pièces jointes (attachments)
- 2 documents téléchargés (liens PDF dans emails)
- 1 document en ligne non téléchargeable (Google Docs)
- 1 transcript meeting (45 min)
- 3 événements calendrier

Valider ?
```
