### Calendar

> Source de capture pour les calendriers.

**Type :** `calendar`

**Statut :** Voir `_SYSTEM/local/sources.md` pour la configuration active.

---

## Configuration

**MCP possibles :** Google Calendar, Outlook Calendar, Apple Calendar

**Accès :**
- [x] Lecture
- [x] Écriture (création/modification événements)
- [ ] Suppression (avec validation)

---

## Comportement

**Ce que l'IA peut faire :**
- Lire les événements pour contexte
- Créer des événements (après validation)
- Proposer des créneaux
- Détecter les conflits
- Rappeler les échéances

**Ce que l'IA ne fait JAMAIS :**
- Supprimer un événement sans confirmation
- Modifier un événement partagé sans validation
- Inviter des participants sans accord

**Règles spécifiques :**
- Événements liés à un projet → mentionner dans l'index
- Échéances importantes → PENDING si action requise
- RDV avec contact → vérifier/créer la fiche

---

## Sync

**Fréquence :** `session` (à chaque démarrage)

**Critères de récupération :**
- Période : aujourd'hui + 7 jours à venir
- Filtres : tous les calendriers actifs

---

## Notes

_Les configurations spécifiques sont dans `local/sources.md`._
