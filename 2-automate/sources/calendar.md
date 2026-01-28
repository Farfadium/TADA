### Calendar

> Source de capture pour les calendriers.

**Type :** `calendar`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

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
- Échéances importantes → noter dans le projet concerné
- RDV avec contact → vérifier/créer la fiche

---

## Sync

**Fréquence :** `session` (à chaque démarrage)

**Critères de récupération :**
- Période : aujourd'hui + 7 jours à venir
- Filtres : tous les calendriers actifs

---

## Actions sync

À chaque sync, l'IA :
1. Récupère les événements J à J+7
2. Pour chaque événement :
   - Identifie le projet lié (titre, participants)
   - Si projet trouvé → vérifier cohérence avec index
   - Si contact présent → vérifier/proposer fiche
3. Détecte les échéances critiques (< 3 jours)
4. Affiche : "📅 X événements cette semaine" + alertes si pertinent

---

## Notes

_Les configurations spécifiques sont dans `local/TOOLS.md`._
