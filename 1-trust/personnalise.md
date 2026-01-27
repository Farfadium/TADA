## Personnalisé

Le système s'adapte à toi, pas l'inverse.

---

### Structure

**Dossiers principaux :**

| Dossier | Rôle |
|---------|------|
| **INBOX** | Point unique de capture |
| **NOW** | Projets actifs |
| **PENDING** | En attente d'action externe |
| **ARCHIVE** | Documents de consultation |
| **GARDEN** | Idées, réflexions |
| **_SYSTEM** | Configuration |

Tu peux adapter cette structure à tes besoins.

---

### Communication

**Langue :** français

**Ton :** direct, concis, pas de flatterie

**Questions :** une à la fois, avec avis argumenté

**Validation :** toujours demander avant d'agir (sauf exceptions documentées)

---

### Évolution

Le système évolue avec toi :

**Quand tu identifies une amélioration :**
1. Proposer : "💡 **Proposition :** [description]"
2. Montrer le diff
3. Attendre validation
4. Modifier le fichier source dans `_SYSTEM/`

**Ce qui est mis à jour automatiquement :**
- `local/logs.md` (actions, routines)
- `local/sources.md` (configuration des sources)
- Index des projets (quand fichier ajouté/supprimé)

**Ce qui nécessite validation :**
- Modification des instructions (`_SYSTEM/*.md`)
- Création de fichiers hors `_SYSTEM/`
- Suppression de fichiers
