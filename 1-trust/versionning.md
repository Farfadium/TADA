## Versionning

Tu versionnes les documents importants pour garder un historique.

### Versionning de fichiers

**Convention de nommage — tu appliques :**
- Format : `YYYY-MM-DD_HHMM_NomDocument.ext`
- La date/heure = moment de création ou de modification significative
- Exemple : `2026-01-26_1430_Compromis.pdf`

**Avant d'enregistrer un fichier, tu vérifies :**
1. Existe-t-il une version précédente du même document ?
2. Si oui :
   - Créer le dossier `_NomDocument/` s'il n'existe pas
   - Déplacer l'ancienne version dans ce dossier
   - Enregistrer la nouvelle version avec la date du jour

**Tu versionnes quand :**
- Nouvelle version reçue d'un tiers
- Modification majeure avant envoi
- Avant signature/validation

**Exemple de structure :**
```
Projet Achat Maison/
├── 2026-01-20_1430_Compromis.pdf      ← Version courante
└── _Compromis/
    └── 2026-01-10_0915_Compromis.pdf  ← Version précédente
```

### Versionning des conversations Claude

Toutes les conversations avec Claude Code sont archivées automatiquement.

**Emplacement :** `_SYSTEM/local/Claude_logs/`

**Mécanisme :**
- Claude Code sauvegarde chaque conversation dans `~/.claude/projects/`
- Un symlink redirige vers `_SYSTEM/local/Claude_logs/`
- Format : JSONL (une ligne JSON par message)
- Nommage : `{session_id}.jsonl`

**Contenu des transcripts :**
- Messages utilisateur
- Réponses Claude
- Appels d'outils (Read, Edit, Bash, etc.)
- Résultats des outils

**Symlink :**
```
~/.claude/projects/-Users-...-TADA → _SYSTEM/local/Claude_logs/
```

### Versionning Git

Le système TADA est versionné avec Git. Tu n'as pas besoin de gérer Git directement.

**Deux repos :**
| Repo | Contenu | Visibilité |
|------|---------|------------|
| `TADA` | `_SYSTEM/` (template) | Public |
| `TADA-YVAN` | Tout le système | Privé |

**Structure :**
- `.git/` stocké dans `~/Documents/Git/` (hors Google Drive)
- Git LFS pour les fichiers binaires (PDF, images, vidéos)
