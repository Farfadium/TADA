---
description: Configuration source Email — règles de sync, labellisation Gmail, archivage emails importants, téléchargement PJ
---

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
---
id: MESSAGE_ID
thread_id: THREAD_ID
date: YYYY-MM-DD
from: Prénom Nom <email@exemple.com>
to: destinataires
subject: Sujet
reply_to: [[emails/YYYY/YYYY-MM-DD_Message_Precedent.md]]  # Si réponse
---

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

[Contenu du message — SANS l'historique quoté]

---

## PJ
- [[attachments/YYYY/Nom_fichier.pdf]] — description
```

---

## Gestion des threads (historique)

**Règle critique** : Ne JAMAIS dupliquer le contenu des messages précédents.

Quand un email contient l'historique (citations ">" ou "Le XX/XX, Untel a écrit:") :
1. **Supprimer** tout l'historique quoté du contenu
2. **Créer un lien** vers le message précédent dans le frontmatter : `reply_to: [[chemin/message.md]]`
3. Le thread est ainsi reconstitué par les liens, sans duplication

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

---

## Pièces jointes

**Règles de téléchargement :**
```bash
gog gmail download-attachment MESSAGE_ID ATTACHMENT_ID --out DESTINATION --account EMAIL
```

**Organisation :**
- Stockées dans `DATA/PENDING/attachments/YYYY/` (collecte)
- Ou dans `DATA/NOW/[Projet]/_emails/` (archivage projet)
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
- DOCX : utiliser `pandoc` ou parser le XML
- XLSX : extraire en CSV ou décrire le contenu
- Images : description si pertinent

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

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (Gmail Pub/Sub, Microsoft Graph)
- [x] Polling API (avec historyId/syncToken)
- [ ] Sync manuelle uniquement

**Gmail Push Notifications (recommandé) :**
```bash
# 1. Créer un topic Pub/Sub dans Google Cloud
# 2. Donner accès au service account Gmail

# Activer le watch
POST https://gmail.googleapis.com/gmail/v1/users/me/watch
Authorization: Bearer $ACCESS_TOKEN
Content-Type: application/json

{
  "topicName": "projects/myproject/topics/gmail-push",
  "labelIds": ["INBOX"]
}
```

**Microsoft Graph (Outlook) :**
```bash
POST https://graph.microsoft.com/v1.0/subscriptions
{
  "changeType": "created",
  "notificationUrl": "https://your-domain.com/webhook/outlook",
  "resource": "/me/mailFolders/inbox/messages",
  "expirationDateTime": "2024-07-20T18:00:00Z"
}
```

**IMAP IDLE (polling amélioré) :**
```python
import imaplib
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(user, password)
mail.select('INBOX')
mail.idle()  # Attend les nouveaux messages
```

**Polling avec historyId :**
```bash
# Gmail - changements depuis historyId
GET https://gmail.googleapis.com/gmail/v1/users/me/history?startHistoryId=$HISTORY_ID
```

**Setup requis :**
1. Gmail : Topic Pub/Sub + watch API
2. Outlook : Subscription Microsoft Graph
3. Renouveler les watches avant expiration (7 jours Gmail)

**Fréquence recommandée :**
- Push : temps réel
- Polling : toutes les 5 minutes

## Notes

_Les configurations spécifiques (Gmail, Outlook, etc.) sont dans `local/TOOLS.md`._
