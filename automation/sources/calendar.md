---
description: Configuration source Calendrier — sync événements, rappels échéances, détection conflits
---

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

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (Google Pub/Sub, Microsoft Graph)
- [x] Polling API (events list avec syncToken)
- [ ] Sync manuelle uniquement

**Google Calendar Push (recommandé) :**
```bash
# Créer un watch sur les événements
POST https://www.googleapis.com/calendar/v3/calendars/primary/events/watch
Authorization: Bearer $ACCESS_TOKEN
Content-Type: application/json

{
  "id": "unique-channel-id",
  "type": "web_hook",
  "address": "https://your-domain.com/webhook/calendar"
}
```

**Microsoft Graph (Outlook) :**
```bash
# Subscription pour changements calendrier
POST https://graph.microsoft.com/v1.0/subscriptions
{
  "changeType": "created,updated,deleted",
  "notificationUrl": "https://your-domain.com/webhook/outlook",
  "resource": "/me/events"
}
```

**Apple Calendar (CalDAV) :**
- Pas de push natif
- Polling avec CalDAV REPORT
- Ou watcher filesystem sur ~/Library/Calendars

**Polling avec syncToken :**
```bash
# Google Calendar
GET https://www.googleapis.com/calendar/v3/calendars/primary/events?syncToken=$TOKEN
```

**Setup requis :**
1. Configurer webhook selon provider
2. Stocker syncToken/deltaLink
3. Renouveler les subscriptions avant expiration

**Fréquence recommandée :**
- Push : temps réel
- Polling : toutes les 15-30 minutes

---

## Notes

_Les configurations spécifiques sont dans `local/TOOLS.md`._
