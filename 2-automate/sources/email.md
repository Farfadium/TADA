### Email

> Source de capture pour les emails.

**Type :** `email`

**Statut :** Voir `_SYSTEM/local/sources.md` pour la configuration active.

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
- Labels/dossiers = projets actifs dans `NOW/`
- Pièces jointes → dossier du projet ou INBOX
- Email non routé → reste dans inbox email + copie dans INBOX/

---

## Sync

**Fréquence :** `session` (à chaque démarrage)

**Critères de récupération :**
- Depuis : dernière sync (voir `local/sources.md`)
- Filtres : inbox uniquement, non traités

---

## Notes

_Les configurations spécifiques (Gmail, Outlook, etc.) sont dans `local/sources.md`._
