---
description: Configuration source Messagerie — capture messages WhatsApp/Telegram/Slack, extraction informations importantes
---

### Messaging

> Source de capture pour les messageries instantanées.

**Type :** `messaging`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

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

## Actions sync

À chaque sync (si source active), l'IA :
1. Récupère les messages non lus depuis dernière sync
2. Pour chaque conversation :
   - Identifie le projet concerné
   - Extrait infos importantes (dates, décisions, fichiers)
   - Si fichier partagé → proposer de télécharger
3. Affiche : "💬 X messages non lus" + résumé si pertinent

---

## Notes

_Les configurations spécifiques sont dans `local/TOOLS.md`._
