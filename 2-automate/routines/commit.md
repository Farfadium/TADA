# Routine : Commit

## Déclencheur

| Type | Valeur |
|------|--------|
| Tag | `#commit`, `#sync`, `#save` |
| Intention | `commit`, `sync`, `enregistre`, `sauvegarde`, `push`, `git` |
| Logique | Modifications significatives effectuées par Claude |

**Impact :** Externe

**Déclenchement automatique :**
Tu déclenches cette routine toi-même quand :
- Tu as fait des modifications significatives (nouveau fichier, édition importante)
- Tu as modifié plusieurs fichiers dans la session
- Tu as terminé une tâche demandée par l'utilisateur qui impliquait des changements
- En fin de session si des changements non commités existent

## Actions

### 1. Vérifier l'état du submodule _SYSTEM

```
cd _SYSTEM && git status
```

Si des changements existent :
1. Stager tous les fichiers : `git add -A`
2. Commiter avec un message descriptif
3. Push : `git push`
4. Revenir au repo principal

### 2. Vérifier l'état du repo principal

```
git status
```

### 3. Analyser les changements

- Identifier les fichiers modifiés
- Grouper par type de changement (config, docs, features, fix)
- Ignorer les fichiers auto-générés (.obsidian/) sauf si explicitement demandé

### 4. Stager les fichiers pertinents

- Stager `_SYSTEM` si le submodule a été commité
- Stager les fichiers de configuration modifiés
- Stager les fichiers de contenu modifiés
- **Ne pas stager** les fichiers .obsidian/ (état workspace)

### 5. Créer le commit

Format du message :
```
type: description courte

- Détail 1
- Détail 2

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

Types :
- `config` : modifications de configuration
- `docs` : documentation, instructions
- `feat` : nouvelle fonctionnalité
- `fix` : correction
- `refactor` : restructuration

### 6. Push

```
git push
```

### 7. Confirmer

Afficher le résultat : `git log -1 --oneline` et statut du push

## Notes

- **AUCUNE VALIDATION DEMANDÉE** : tu exécutes le commit directement sans demander confirmation
- Tu affiches un résumé des changements et le message de commit, puis tu commits immédiatement
- Les fichiers non trackés sont ajoutés automatiquement si pertinents (sauf .obsidian/)
- Si le submodule a des changements, il est TOUJOURS commité en premier
- En cas d'erreur ou conflit uniquement, tu demandes de l'aide
