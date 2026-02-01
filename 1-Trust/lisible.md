## Lisible

Tout est traçable, consultable, indépendant.

---

### Historique

**Versionning des fichiers :**
- Convention : `YYYY-MM-DD_HHMM_NomDocument.ext`
- Anciennes versions dans `_NomDocument/`
- Tu versionnes quand : nouvelle version reçue, modification majeure, avant signature

**Versionning des conversations :**
- Emplacement : `_SYSTEM/local/Claude_logs/`
- Format : JSONL (une ligne JSON par message)
- Contenu : messages, réponses, appels d'outils

**Logs des actions :**
- Emplacement : `_SYSTEM/local/logs.md`
- Contenu : routines exécutées, décisions utilisateur, actions significatives

---

### Formats ouverts

**Texte :** Markdown (`.md`)
- Lisible par tous, indépendant de l'outil
- Compatible Obsidian, VS Code, n'importe quel éditeur

**Documents :** PDF, Word, Excel
- Stockés tels quels
- Gérés par Git LFS

**Structure :** Dossiers + fichiers
- Pas de base de données
- Tout est navigable dans le Finder

---

### Indépendance

Le système fonctionne sans IA :
- Les index expliquent chaque dossier
- Les liens connectent les informations
- L'historique est consultable

L'IA accélère, elle ne remplace pas.
