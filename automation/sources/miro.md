---
description: Configuration source Miro — export boards, récupération contenus visuels, archivage workshops/brainstorms
---

### Miro

> Boards collaboratifs visuels — workshops, brainstorms, planification.

**Type :** `collaboration`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**API disponible :** Board Export API (developers.miro.com)

**Formats d'export :**
- ZIP contenant :
  - Board content : SVG, PDF ou HTML
  - JSON : commentaires
  - JSON : liste des users (viewers/editors)
  - Vidéos TalkTrack (si applicable)
  - JSON : metadata du board

**Prérequis :**
- Plan Enterprise (requis pour API)
- Rôle Company Admin
- eDiscovery activé dans Settings

**Limites :**
- 1000 boards max par job d'export
- 1 job simultané (Enterprise) ou 5 jobs (Enterprise Guard)
- Lien de téléchargement valide 15 minutes

**Accès :**
- [x] Lecture (via API)
- [ ] Écriture
- [ ] Suppression

---

## Comportement

**Ce que l'IA peut faire :**
- Lister les boards accessibles
- Exporter un board en PDF/HTML/SVG
- Récupérer les commentaires d'un board
- Identifier les participants à un board
- Archiver les boards importants dans les projets

**Ce que l'IA ne fait JAMAIS :**
- Modifier un board sans permission explicite
- Supprimer des boards
- Partager des boards avec des tiers
- Exfiltrer du contenu confidentiel

**Règles spécifiques :**
- Les boards contiennent souvent du contenu confidentiel (stratégie, brainstorms)
- Toujours vérifier le contexte avant d'archiver
- Boards liés à un projet → proposer d'archiver dans le projet

---

## Sync

**Fréquence :** `manuel` (sur demande uniquement)

**Raisons :**
- API Enterprise uniquement
- Export lourd (ZIP avec assets)
- Pas de webhook disponible
- Utilisation ciblée sur boards spécifiques

**Workflow de récupération :**
1. L'utilisateur identifie un board important
2. L'IA exporte le board via l'API
3. Téléchargement et extraction du ZIP
4. Archivage dans le projet concerné

---

## Actions sync

Quand l'utilisateur demande de récupérer un board Miro :
1. Récupérer l'ID ou URL du board
2. Lancer un job d'export via l'API (format PDF + JSON commentaires)
3. Attendre la fin du job (asynchrone)
4. Télécharger le ZIP
5. Extraire le contenu dans `DATA/NOW/[Projet]/_miro/`
6. Créer un fichier `.md` récapitulatif avec :
   - Screenshot ou lien vers le PDF
   - Résumé des commentaires clés
   - Participants
   - Date et contexte

---

## Archivage des boards importants

**Quand archiver un board :**
- Workshop stratégique
- Session de brainstorming avec décisions
- Planification de projet
- Roadmap visuelle
- Résultat de session collaborative importante

**Format Markdown :**
```markdown
# [Nom du board]

- **Date :** YYYY-MM-DD
- **Board ID :** [ID Miro]
- **Lien :** [URL du board Miro](https://miro.com/app/board/XXX)
- **Participants :** [[Prénom Nom]], [[Prénom Nom]], ...
- **Type :** Workshop / Brainstorm / Planning / Autre

## Résumé
[2-3 phrases : ce qui s'est passé, objectif du board]

## Pourquoi c'est important
[1-2 phrases : impact sur le projet, décisions clés]

## Décisions / Actions clés
- Décision 1
- Action item @[[Prénom Nom]]

## Commentaires importants

> Citation importante
> — [[Prénom Nom]]

---

## Fichiers exportés

- [Board.pdf](Board.pdf) — Export visuel complet
- [Comments.json](Comments.json) — Tous les commentaires
- [Metadata.json](Metadata.json) — Infos du board

---

## Notes
[Contexte additionnel, liens vers d'autres documents]
```

**Emplacement :** `DATA/NOW/[Projet]/_miro/YYYY-MM-DD_Nom-board.md`

**Avant d'archiver — vérifications obligatoires :**
1. **Vérifier les doublons** : `Glob _miro/*` pour s'assurer que le board n'existe pas déjà
2. **Créer les fiches People** manquantes pour tous les participants
3. Créer le dossier `_miro/YYYY-MM-DD_Nom-board/` avec les fichiers exportés
4. Créer le fichier `.md` avec liens `[[Prénom Nom]]`

**Règles :**
- Toujours créer les liens `[[Prénom Nom]]` vers les fiches People
- Stocker le PDF et les JSON dans un sous-dossier dédié
- Le lien Miro permet de retrouver le board original
- Ne jamais dupliquer un board déjà archivé

---

## Recherche de boards pour un projet

**Workflow manuel (pas de search API disponible) :**
1. Demander à l'utilisateur de fournir les URLs/IDs des boards pertinents
2. Ou : l'utilisateur partage une liste de boards depuis Miro
3. Pour chaque board identifié :
   - Vérifier s'il n'est pas déjà archivé
   - Exporter si pertinent
   - Archiver dans le projet

**Alternative (si pas d'accès API) :**
- Export manuel par l'utilisateur (File > Export > PDF ou HTML)
- Upload du fichier dans TADA
- Création du fichier `.md` récapitulatif par l'IA

---

## Notes

**API vs Export manuel :**
- Si plan Enterprise : utiliser l'API pour automatiser
- Sinon : export manuel + upload dans TADA

**Stockage des assets :**
- Les fichiers PDF/images peuvent être lourds
- Stocker dans `_miro/[nom-board]/` pour garder organisé
- Créer un fichier `.md.md` à côté de chaque PDF pour le rendre searchable

_Les configurations spécifiques (tokens API, etc.) sont dans `local/TOOLS.md`._