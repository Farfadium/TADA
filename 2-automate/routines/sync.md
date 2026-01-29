---
A quoi sert ce fichier: Routine de diagnostic système au démarrage — vérifie l'état de DATA/NOW/, DATA/INBOX/, sources actives et propose actions prioritaires adaptées au contexte
---

### Sync

> Diagnostic système + propositions adaptées à l'état actuel.

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Temps | Début de session |
| Tag | #sync |

---

## Actions

### 1. Diagnostic système

| Vérification | État |
|--------------|------|
| DATA/NOW/ | Projets actifs ? |
| DATA/INBOX/ | Décision humaine requise ? |
| Sources | Configurées et syncées ? |

### 2. Déterminer la priorité

| État du système | Priorité |
|-----------------|----------|
| DATA/NOW/ vide | Initialiser les projets |
| Projets sans labels Gmail | Configurer la correspondance |
| DATA/INBOX/ non vide | Trier les fichiers |
| Système prêt + emails non lus | Trier les emails |

### 3. Output

```
**Sync** | [état système en 1 ligne]

[diagnostic court]

→ Par quoi on commence ?
1. [action prioritaire] (recommandé)
2. [autre action possible]
3. [autre action possible]
```

---

## Validation

**Sans validation :** diagnostic, lecture des sources
**Avec validation :** toute action proposée

---

## Maintenance (si système opérationnel)

À faire en arrière-plan si le système est déjà configuré :

| Vérification | Action |
|--------------|--------|
| Index obsolètes | Nettoyer les entrées orphelines |
| Fichiers non listés | Ajouter aux index |
| Dernière vérification | Mettre à jour avec date+heure dans `local/TOOLS.md` |

**Note :** "Inbox 0" n'est mis à jour que lorsque tous les éléments d'une source ont été traités (routine tri terminée).
