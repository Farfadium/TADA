---
A quoi sert ce fichier: Ajout d'une règle système — modifie les fichiers de _SYSTEM/ pour documenter et systématiser un nouveau comportement demandé par l'utilisateur
---

### Ajout règle

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Tag | #rule |

**Impact :** Système

**Contexte :**
Quand l'utilisateur identifie un comportement à systématiser, il demande l'ajout d'une règle dans CLAUDE.md.

**Actions :**

1. Comprendre la règle à ajouter
2. Identifier le fichier cible dans `_SYSTEM/` :
   - Nouvelle routine → `2-Automate/routines/`
   - Règle de capture → `1-Trust/`
   - Règle de documentation → `3-Document/`
   - Préférence utilisateur → `1-Trust/SOUL.md` ou `4-Act/proactivite.md`
3. Rédiger la modification
4. Montrer le diff complet
5. Attendre validation explicite
6. Appliquer et regénérer CLAUDE.md

**Validation requise :** Oui (obligatoire, diff complet)

**Exemple :**
```
#rule Toujours proposer 3 noms de fichiers alternatifs

→ Ajout proposé dans _SYSTEM/1-Trust/capture.md :

+ **Convention de nommage :**
+ - Toujours proposer 3 alternatives de noms de fichiers
+ - L'utilisateur choisit ou propose un autre nom

Valider ?
```

**Après validation :**
- Modifier le fichier source
- Exécuter `build-claude-md.sh` pour regénérer CLAUDE.md
