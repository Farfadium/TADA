## Maintenance

Le système s'auto-maintient. L'IA apprend et évolue.

---

### Auto-évolution

**Quand tu apprends quelque chose, tu le documentes :**

| Information apprise | Fichier à mettre à jour |
|--------------------|------------------------|
| Règle sur une source (email, etc.) | `2-Automate/sources/[source].md` (notes) |
| Configuration spécifique | `local/sources.md` |
| Préférence utilisateur | Fichier concerné dans `_SYSTEM/` |
| Résultat de routine | `local/logs.md` |
| Décision utilisateur | `local/logs.md` (section Décisions) |

**Exemple :**
> Utilisateur : "Les emails de newsletters, archive-les directement"

→ Tu ajoutes dans `local/sources.md` :
```
**Règle :** Newsletters → archiver sans validation
```

---

### Logging

**Ce qui est loggé automatiquement :**
- Exécution de routines (date, résultat)
- Décisions utilisateur (proposition, réponse)
- Actions significatives

**Voir :** `_SYSTEM/2-Automate/logs.md` pour le format détaillé.

---

### Nettoyage automatique

**Routines non utilisées :**
- Si une routine n'a pas été exécutée depuis 60 jours → proposer suppression
- Logger la proposition et la réponse

**Sources non utilisées :**
- Si une source est configurée mais jamais syncée → alerter
- Proposer de la désactiver ou de la configurer correctement

**Index obsolètes :**
- Fichiers listés mais supprimés → nettoyer l'index
- Fichiers présents mais non listés → ajouter à l'index

---

### Règles de mise à jour

**Sans validation :**
- `local/logs.md`
- `local/sources.md` (date de sync)
- Index (`*/index.md`) : ajout/suppression de fichiers listés

**Avec validation :**
- Instructions dans `_SYSTEM/*.md`
- Fichiers utilisateur hors `_SYSTEM/`
- Suppression de fichiers
- Création de nouvelles règles
