### Messaging

> Source de capture pour les messageries instantanées.

**Type :** `messaging`

**Statut :** Voir `_SYSTEM/local/sources.md` pour la configuration active.

---

## Configuration

**MCP possibles :** WhatsApp, Telegram, Slack, Discord, iMessage

**Accès :**
- [x] Lecture
- [x] Écriture (messages)
- [ ] Suppression (jamais automatique)

---

## Comportement

**Ce que l'IA peut faire :**
- Lire les messages pour capture
- Extraire les informations importantes (dates, décisions, fichiers)
- Proposer des réponses
- Envoyer des messages (après validation)

**Ce que l'IA ne fait JAMAIS :**
- Envoyer sans validation explicite
- Supprimer des messages
- Rejoindre/quitter des groupes

**Règles spécifiques :**
- Fichiers partagés → INBOX ou dossier projet
- Informations importantes → mettre à jour l'index du projet
- Conversations de groupe → identifier le projet concerné

---

## Sync

**Fréquence :** `manuel` (sur demande)

**Critères de récupération :**
- Depuis : dernière sync
- Filtres : conversations actives, non lus

---

## Notes

_Les configurations spécifiques sont dans `local/sources.md`._
