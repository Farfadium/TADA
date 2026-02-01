# CONTRIBUTING.md — Règles de contribution

> Comment travailler sur _SYSTEM/ de façon propre.

---

## Philosophie

- **DATA/** = ta vie → toujours sur `main`, jamais de branche
- **_SYSTEM/** = le système → branches pour les gros chantiers risqués

---

## Quand rester sur main

✅ **Changements additifs** (nouveau composant, nouvelle feature) :
- Ajouter un nouveau dossier (ex: TADA-WEB)
- Ajouter une nouvelle source
- Ajouter de la documentation
- Corrections mineures

→ Pas de risque de casser l'existant, on reste sur main.

---

## Quand créer une branche

⚠️ **Changements destructifs** (refacto, restructuration) :
- Changer la structure des dossiers existants
- Modifier le format des fichiers
- Refactoring majeur
- Migration de données
- Expérimentation risquée

→ Créer une branche, tester dans un worktree, merger quand validé.

---

## Git Worktrees

### Concept

Au lieu de switcher de branche, créer une copie de travail parallèle :

```bash
# Créer un worktree pour une feature
git worktree add ../tada-system-refacto -b feature/refacto-structure

# Travailler dessus
cd ../tada-system-refacto
# ... faire les changements ...

# Quand c'est prêt, merger
git checkout main
git merge feature/refacto-structure

# Nettoyer
git worktree remove ../tada-system-refacto
git branch -d feature/refacto-structure
```

### Avantages

- Travail parallèle sans perdre le contexte
- Tester sans impacter main
- Plusieurs agents peuvent travailler en parallèle

### Quand utiliser

| Situation | Action |
|-----------|--------|
| Petit fix | Commit direct sur main |
| Nouvelle feature additive | Commit sur main |
| Gros refacto | Worktree + branche |
| Expérimentation | Worktree + branche |
| Travail parallèle (2+ agents) | Worktrees séparés |

---

## Naming conventions

### Fichiers et dossiers — RÈGLES STRICTES

**Compatibilité cross-platform (Mac, Linux, Windows, Google Drive) :**

| ❌ Interdit | ✅ Correct |
|-------------|-----------|
| Espaces | Tirets `-` ou underscores `_` |
| Accents (é, è, ê, à, ô, etc.) | Sans accents (e, a, o) |
| Caractères spéciaux (`?`, `*`, `:`, `<`, `>`, `\|`) | Aucun |
| Apostrophes, guillemets | Aucun |

**Exemples :**
| ❌ Mauvais | ✅ Bon |
|------------|--------|
| `Les Jaunets` | `Les-Jaunets` |
| `Déclic CNV` | `Declic-CNV` |
| `Impôts` | `Impots` |
| `idées` | `idees` |
| `A traiter` | `A-traiter` |

**Convention _SYSTEM :**
- Préfixes numériques : `1-Trust`, `2-Automate`, `3-Document`, `4-Act`
- PascalCase pour les dossiers principaux
- kebab-case ou snake_case pour les sous-dossiers

**Convention DATA :**
- PascalCase pour les projets : `Les-Jaunets`, `TADA-PROJECT`
- Dates en préfixe : `YYYY-MM-DD_Sujet.md`

### Branches

```
feature/nom-court       # Nouvelle fonctionnalité
refacto/nom-court       # Restructuration
fix/nom-court           # Correction
experiment/nom-court    # Test/expérimentation
```

### Worktrees

```
../tada-[nom-branche]   # À côté du repo principal
```

---

## Process de merge

1. **Tester** dans le worktree
2. **Commit** tous les changements
3. **Revenir sur main** : `git checkout main`
4. **Merger** : `git merge feature/xxx`
5. **Résoudre** les conflits si nécessaire
6. **Pusher** : `git push`
7. **Nettoyer** : `git worktree remove` + `git branch -d`

---

## Pour l'agent (moi)

### Comportement attendu

- **Par défaut** : travailler sur main
- **Proposer un worktree** si :
  - Le changement touche à la structure existante
  - Le travail va prendre plusieurs sessions
  - Il y a un risque de casser quelque chose
  - L'utilisateur demande une expérimentation

### Comment proposer

> "Ce changement touche à [X]. Je propose de créer une branche `feature/xxx` pour ne pas impacter main. OK ?"

Si oui → créer le worktree et travailler dessus.

---

## État actuel

| Composant | Branche | Statut |
|-----------|---------|--------|
| Core _SYSTEM | main | Stable |
| Sources (docs) | main | En cours (additif) |
| TADA-WEB | main | WIP (additif) |
| Bootstrap | main | En définition |

---

*Ces règles s'appliquent à _SYSTEM/. Pour DATA/, tout reste toujours sur main.*
