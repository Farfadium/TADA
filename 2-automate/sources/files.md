### Files

> Source de capture pour les fichiers déposés.

**Type :** `files`

**Statut :** `actif` (natif, pas de MCP requis)

---

## Configuration

**MCP requis :** aucun (accès direct au système de fichiers)

**Accès :**
- [x] Lecture
- [x] Écriture
- [x] Déplacement
- [ ] Suppression (avec validation)

---

## Comportement

**Ce que l'IA peut faire :**
- Lire les fichiers dans INBOX/
- Proposer le routage vers le bon dossier
- Renommer selon les conventions
- Créer des versions (versionning)
- Extraire les métadonnées

**Ce que l'IA ne fait JAMAIS :**
- Supprimer un fichier sans confirmation
- Écraser un fichier sans versionning
- Modifier un fichier hors _SYSTEM sans validation

**Règles spécifiques :**
- Nouveau fichier dans INBOX → proposer routage
- Fichier avec date → appliquer convention YYYY-MM-DD_HHMM_Nom
- Fichier similaire existant → proposer versionning

---

## Sync

**Fréquence :** `session` (à chaque démarrage)

**Critères de récupération :**
- Dossier : INBOX/
- Filtres : fichiers non traités (pas dans un sous-dossier projet)

---

## Notes

_Source toujours active, pas de configuration requise._
