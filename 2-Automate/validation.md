---
A quoi sert ce fichier:
Règles de validation — Définit quelles actions peuvent être faites sans validation (lecture, routage INBOX) et lesquelles nécessitent confirmation (suppression, envoi email)
---

## Validation

Le système propose, l'humain valide — mais pas pour tout.

---

### Actions SANS validation

Ces actions peuvent être exécutées directement :

| Action | Périmètre | Condition |
|--------|-----------|-----------|
| **Lire** un fichier | Tout TADA | — |
| **Créer** un fichier | `DATA/INBOX/` | — |
| **Modifier** un fichier | `_SYSTEM/` | Sauf `instructions.md` |
| **Modifier** un index | `*/index.md` | Ajout/suppression de fichier listé |
| **Déplacer** un fichier | `DATA/INBOX/` → ailleurs | Routage évident |
| **Régénérer** `claude.md` | — | Après modif dans `_SYSTEM/` |
| **Exécuter** une routine | — | Déclenchée par tag |
| **Commit** git | — | Quand un ensemble cohérent de modifications est terminé |

---

### Actions AVEC validation

Ces actions nécessitent toujours une confirmation :

| Action | Raison |
|--------|--------|
| **Supprimer** un fichier | Irréversible |
| **Modifier** `instructions.md` | Impact sur le comportement global |
| **Envoyer** un email | Action externe |
| **Modifier** un fichier hors `_SYSTEM/` | Données utilisateur |
| **Créer** une fiche (annuaires) | Demander du contexte et des informations à ajouter |

---

### Format de validation

Quand une validation est requise :

```
**Action :** [description courte]

[diff ou aperçu]

Valider ?
```

**Réponses acceptées :** `oui`, `go`, `ok`, `yes`, `valide`, `1`

---

### Cas particuliers

**Modifications multiples :**
Si plusieurs fichiers doivent être modifiés ensemble → montrer la liste, une seule validation pour l'ensemble.

**Doute :**
En cas de doute sur la catégorie → demander validation.

**Tu ne fais JAMAIS :**
- Envoyer un email directement (toujours brouillon d'abord)
- Supprimer un fichier sans confirmation explicite
- Poser plusieurs questions à la fois
