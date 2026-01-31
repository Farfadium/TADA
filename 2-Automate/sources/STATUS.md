# État des Sources — Suivi de collecte

> Mise à jour par le Collecteur à chaque run.

_Dernière mise à jour : 2026-01-31 22:25 UTC_

## Vue globale

| Source | Statut | Dernière sync | Volume | Couverture | Problèmes |
|--------|--------|---------------|--------|------------|-----------|
| **Gmail** | ⚠️ Partiel | 2026-01-30 | 12,567 emails | 2022→2026 | Attachments incomplets |
| **Calendar** | ✅ Complet | 2026-01-30 | 42,321 events | 2024-06→2026-02 | — |
| **Fireflies** | ✅ Complet | 2026-01-30 | 1,467 transcripts | 2021-06→2026-01 | — |
| **Folk CRM** | ✅ Complet | 2026-01-30 | 300 contacts | Snapshot | — |
| **Miro** | ⚠️ Partiel | 2026-01-30 | 196 boards | 2020→2026 | Rate limit, 17 boards manquants |

## Légende

| Statut | Signification |
|--------|---------------|
| ✅ Complet | Toutes les données récupérées |
| ⚠️ Partiel | Données incomplètes, action requise |
| ❌ Erreur | Source cassée, intervention urgente |
| 🔄 En cours | Sync en cours |
| ⏸️ Pause | Source désactivée temporairement |

## Actions requises

### Gmail — Attachments manquants
- **Problème** : 215 attachments téléchargés sur ~850 emails avec PJ
- **Estimation** : ~635 attachments manquants
- **Action** : Relancer le téléchargement des PJ

### Miro — Rate limit
- **Problème** : 196/213 boards récupérés
- **Action** : Attendre reset rate limit, relancer

## Historique

| Date | Source | Action | Résultat |
|------|--------|--------|----------|
| 2026-01-30 | Gmail | Collecte initiale | 12,567 emails |
| 2026-01-30 | Calendar | Collecte initiale | 42,321 events |
| 2026-01-30 | Fireflies | Collecte initiale | 1,467 transcripts |
| 2026-01-30 | Folk | Export complet | 300 contacts |
| 2026-01-30 | Miro | Export partiel | 196/213 boards |

---

*Ce fichier est la source de vérité pour l'état des collectes. Voir les fichiers `*-status.json` pour le détail par source.*
