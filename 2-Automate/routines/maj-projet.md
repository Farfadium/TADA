---
A quoi sert ce fichier: Mise à jour d'un projet spécifique — modifie le statut, les tâches et les notes d'un projet suite à un nouvel événement ou information
---

### Mise à jour projet

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Tag | #projet [nom] |

**Impact :** Contenu

**Contexte :**
Mettre à jour un projet spécifique suite à un événement ou une information nouvelle.

**Actions :**

1. Identifier le projet concerné (via le nom après #projet)
2. Lire l'`index.md` du projet dans `DATA/NOW/`
3. Proposer les mises à jour :
   - Statut
   - Tâches (ajouter/compléter)
   - Notes
   - Fichiers associés
4. Appliquer après validation

**Validation requise :** Oui (montrer le diff)

**Exemple :**
```
#projet Achat Maison

Le notaire a confirmé la date de signature.

→ Mise à jour proposée dans DATA/NOW/Achat Maison/index.md :

## Statut
- En cours → **Signature prévue le 15/02**

## À faire
+ [ ] Préparer les fonds pour le 14/02
+ [ ] Confirmer présence à l'étude

Valider ?
```
