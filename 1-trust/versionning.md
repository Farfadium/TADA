## Versionning

Tout est sauvegardé, sécurisé, versionné — à deux niveaux.

### Versionning de fichiers

Pour les documents importants (contrats, protocoles, etc.), on garde un historique explicite.

**Convention de nommage :**
- Format : `YYYY-MM-DD_HHMM_NomDocument.ext`
- La date/heure = moment de création ou de modification significative
- Exemple : `2026-01-26_1430_Compromis.pdf`

**Avant d'enregistrer un fichier :**
1. Vérifier s'il existe une version précédente du même document
2. Si oui :
   - Créer le dossier `_NomDocument/` s'il n'existe pas
   - Déplacer l'ancienne version dans ce dossier (avec sa date)
   - Enregistrer la nouvelle version avec la date du jour

**Quand versionner :**
- Nouvelle version reçue d'un tiers
- Modification majeure avant envoi
- Avant signature/validation

**Exemple :**
```
Projet Achat Maison/
├── 2026-01-20_1430_Compromis.pdf      ← Version courante
└── _Compromis/
    └── 2026-01-10_0915_Compromis.pdf  ← Version précédente
```

### Versionning Git

Le système TADA est versionné avec Git pour tracer toutes les modifications.

**Deux repos :**
| Repo | Contenu | Visibilité |
|------|---------|------------|
| `TADA` | `_SYSTEM/` (template) | Public |
| `TADA-YVAN` | Tout le système | Privé |

**Structure :**
- `.git/` stocké dans `~/Documents/Git/` (hors Google Drive)
- Git LFS pour les fichiers binaires (PDF, images, vidéos)
