### Email

> Source de capture pour les emails.

**Type :** `email`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**MCP possibles :** Gmail, Outlook, IMAP générique

**Accès :**
- [x] Lecture (obligatoire)
- [x] Écriture (brouillons uniquement)
- [ ] Suppression (jamais automatique)

---

## Comportement

**Ce que l'IA peut faire :**
- Lire les emails pour capture et tri
- Créer des brouillons (jamais d'envoi direct)
- Appliquer des labels/dossiers (correspondent aux projets actifs)
- Télécharger les pièces jointes vers le bon dossier
- Proposer des réponses

**Ce que l'IA ne fait JAMAIS :**
- Envoyer un email directement (toujours brouillon → validation → envoi)
- Supprimer un email sans confirmation explicite
- Marquer comme lu sans traitement

**Règles spécifiques :**
- Labels/dossiers = projets actifs dans `DATA/NOW/`
- Pièces jointes → dossier du projet ou INBOX
- Email non routé → reste dans inbox email + copie dans DATA/INBOX/

---

## Sync

**Fréquence :** `session` (à chaque démarrage)

**Critères de récupération :**
- Depuis : dernière sync (voir `local/TOOLS.md`)
- Filtres : inbox uniquement, non traités

---

## Actions sync

À chaque sync, l'IA :
1. Récupère les emails depuis la dernière sync (voir `local/TOOLS.md`)
2. Filtre : inbox, non traités
3. Pour chaque email :
   - Identifie le projet (mots-clés, expéditeur)
   - Si projet trouvé → proposer de labelliser/router
   - Si pièce jointe → proposer de télécharger vers le projet
   - Si non routé → afficher dans le résumé
4. Affiche : "📧 X nouveaux emails" + résumé si pertinent

---

## Archivage des emails importants

**Quand archiver un email :**
- Décision importante (validation, accord, refus)
- Engagement contractuel ou financier
- Information clé pour le projet
- Échange à conserver pour référence future

**Format Markdown :**
```markdown
# [Sujet de l'email]

- **De :** [[Prénom Nom]] (email@exemple.com)
- **À :** Destinataire
- **Date :** YYYY-MM-DD HH:MM
- **Gmail :** [Lien](https://mail.google.com/mail/u/0/#inbox/ID)

## Résumé
[1-2 phrases : ce que dit l'email]

## Pourquoi c'est important
[1-2 phrases : impact sur le projet, décision prise, action requise]

---

[Contenu complet de l'email]

---

## PJ
- [Nom_fichier.pdf](Nom_fichier.pdf) — description
```

**Emplacement :** `DATA/NOW/[Projet]/_emails/YYYY-MM-DD_Sujet_court.md`

**Avant d'archiver :**
1. Vérifier que l'email n'existe pas déjà (Glob `_emails/*Sujet*` ou recherche par date)
2. Pour chaque personne mentionnée (expéditeur, destinataires) :
   - Vérifier si fiche existe dans `DATA/ARCHIVE/Répertoires/People/`
   - Si non → créer la fiche immédiatement
3. Créer le fichier markdown avec liens `[[Prénom Nom]]`

**Règles :**
- Toujours créer les liens `[[Prénom Nom]]` vers les fiches People
- Créer les fiches People manquantes AVANT d'archiver l'email
- Télécharger les PJ dans le même dossier `_emails/`
- Le lien Gmail permet de retrouver l'original si besoin
- Ne jamais dupliquer un email déjà archivé

---

## Notes

_Les configurations spécifiques (Gmail, Outlook, etc.) sont dans `local/TOOLS.md`._
