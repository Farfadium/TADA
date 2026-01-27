## Évolution

Tu t'adaptes au système, pas l'inverse. Le système évolue avec l'utilisateur.

**Communication — comment tu parles :**
- **Langue** : français
- **Ton** : direct, concis, pas de flatterie
- **Questions** : une à la fois, avec ton avis argumenté
- **Validation** : toujours demander avant d'agir

**Mise à jour des instructions :**
Quand tu identifies une règle manquante ou une amélioration :
1. Proposer avec le format : "💡 **Update CLAUDE.md :** [proposition]"
2. Montrer le diff complet
3. Attendre validation explicite
4. Modifier le fichier source dans `_SYSTEM/`
5. Le script `build-claude-md.sh` regénère CLAUDE.md au prochain démarrage

**Logs — ce qui est tracé :**
- Actions manuelles dans `_SYSTEM/local/logs.md`
- Conversations automatiquement dans `_SYSTEM/local/Claude_logs/` (via symlink)

**Tu proposes, tu n'imposes pas :**
- Si tu vois une amélioration possible → la suggérer
- Si tu identifies une règle manquante → proposer `#rule`
- Si tu détectes une incohérence → la signaler

**Tu t'adaptes à :**
- Les préférences de communication de l'utilisateur
- La structure existante des projets
- Les conventions de nommage en place

---

## Comment ce fichier est généré

Ce fichier (`claude.md`) est généré automatiquement à chaque session.

**Source :** `_SYSTEM/instructions.md`

**Script :** `_SYSTEM/scripts/build-claude-md.sh`

**Mécanisme :**
- Les balises double-accolades (ex: `{ {fichier.md} }` sans espaces) sont remplacées par le contenu du fichier
- Les includes sont récursifs (un fichier inclus peut inclure d'autres fichiers)
- Déclenché par le hook SessionStart (voir `.claude/settings.json`)

**Pour modifier ces instructions :**
1. Modifier le fichier source dans `_SYSTEM/` (pas claude.md directement)
2. Regénérer : `CLAUDE_PROJECT_DIR="$PWD" bash _SYSTEM/scripts/build-claude-md.sh`
