### [Nom de la source]

> Template pour configurer une source de capture.

**Type :** `email` | `messaging` | `calendar` | `files` | `meetings` | `other`

**Statut :** Voir `_SYSTEM/local/sources.md` pour la configuration active.

---

## Configuration

**MCP possibles :** [liste des MCP compatibles]

**Accès :**
- [ ] Lecture
- [ ] Écriture
- [ ] Suppression

---

## Comportement

**Ce que l'IA peut faire :**
- ...

**Ce que l'IA ne fait JAMAIS :**
- ...

**Règles spécifiques :**
- ...

---

## Sync

**Fréquence :** `session` | `quotidien` | `manuel`

**Critères de récupération :**
- Depuis : [dernière sync | date fixe | X jours]
- Filtres : [non lu | label | expéditeur | etc.]

---

## Actions sync

À chaque sync, l'IA :
1. Récupère les éléments depuis la dernière sync
2. Pour chaque élément :
   - Identifie le projet concerné
   - Si projet trouvé → proposer d'archiver
3. Affiche un résumé

---

## Archivage (si applicable)

**Quand archiver :**
- [critères pour décider d'archiver un élément]

**Format Markdown :**
```markdown
# [Titre]

- **Date :** YYYY-MM-DD
- **Source :** [lien vers l'original]

## Résumé
[description courte]

## Pourquoi c'est important
[impact sur le projet]

## Notes
[contexte additionnel]
```

**Emplacement :** `NOW/[Projet]/_[type]/YYYY-MM-DD_Titre.md`

**Avant d'archiver — vérifications obligatoires :**
1. **Vérifier les doublons** : `Glob _[type]/*` pour s'assurer que l'élément n'existe pas déjà
2. **Créer les fiches People** manquantes dans `ARCHIVE/Répertoires/People/`
3. Créer le fichier avec liens `[[Prénom Nom]]`

---

## Recherche pour un projet

**Quand l'utilisateur demande de récupérer les éléments d'un projet :**

1. **Lire l'index du projet** pour identifier :
   - Les mots-clés
   - Les parties prenantes
   - Les entreprises impliquées

2. **Rechercher** par :
   - Nom du projet
   - Noms des parties prenantes
   - Termes métier spécifiques

3. **Vérifier les doublons** avant d'archiver

---

## Notes

_Les configurations spécifiques sont dans `local/sources.md`._
