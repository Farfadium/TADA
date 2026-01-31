---
description: Configuration source Meetings (Fireflies) — récupération transcripts, archivage meetings importants, extraction action items
---

### Meetings

> Transcriptions automatiques des réunions via Fireflies.ai.

**Type :** `meetings`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**MCP possibles :** Fireflies.ai, Otter.ai, autres services de transcription

**Accès :**
- [x] Lecture (transcripts, résumés, action items)
- [ ] Écriture
- [ ] Suppression

---

## Comportement

**Ce que l'IA peut faire :**
- Rechercher des meetings par mot-clé, participant, date
- Récupérer les transcripts complets
- Extraire les résumés et action items
- Identifier les participants et speakers
- Archiver les meetings importants dans le projet concerné

**Ce que l'IA ne fait JAMAIS :**
- Supprimer des transcripts
- Partager des transcripts avec des tiers
- Extraire des infos sensibles sans contexte

**Règles spécifiques :**
- Les transcripts contiennent des conversations confidentielles
- Toujours demander le contexte avant d'extraire des informations sensibles
- Meetings liés à un projet → proposer d'archiver dans le projet

---

## Sync

**Fréquence :** `session` (à chaque démarrage)

**Critères de récupération :**
- Depuis : dernière sync (voir `local/TOOLS.md`)
- Filtres : meetings de l'utilisateur

---

## Actions sync

À chaque sync, l'IA :
1. Récupère les meetings depuis la dernière sync
2. Pour chaque meeting récent :
   - Identifie le projet (participants, sujet)
   - Si projet trouvé → proposer d'archiver
   - Si action items → les lister
3. Affiche : "🎙️ X nouveaux meetings" + résumé si pertinent

---

## Archivage des meetings importants

**Quand archiver un meeting :**
- Décision importante prise en réunion
- Action items à suivre
- Information clé pour le projet
- Réunion avec partenaires/clients externes

**Format Markdown :**
```markdown
# [Titre du meeting]

- **Date :** YYYY-MM-DD HH:MM
- **Durée :** X min
- **Participants :** [[Prénom Nom]], [[Prénom Nom]], ...
- **Fireflies :** [Lien](https://app.fireflies.ai/view/ID)

## Résumé
[2-3 phrases : ce qui s'est passé, décisions prises]

## Pourquoi c'est important
[1-2 phrases : impact sur le projet, décision clé, prochaine étape critique]

## Action items
- [ ] @[[Prénom Nom]] — Action à faire
- [ ] @[[Prénom Nom]] — Autre action

## Points clés
- Point important 1
- Point important 2

---

## Transcript (extraits)

> Citation importante du meeting
> — [[Prénom Nom]]

[Extraits pertinents du transcript, pas la totalité]

---

## Notes
[Contexte additionnel, liens vers d'autres documents]
```

**Emplacement :** `DATA/NOW/[Projet]/_meetings/YYYY-MM-DD_Titre_court.md`

**Avant d'archiver :**
1. Vérifier que le meeting n'existe pas déjà (Glob `_meetings/*Titre*` ou recherche par date)
2. Pour chaque participant mentionné :
   - Vérifier si fiche existe dans `DATA/ARCHIVE/Répertoires/People/`
   - Si non → créer la fiche immédiatement
3. Créer le fichier markdown avec liens `[[Prénom Nom]]`

**Règles :**
- Toujours créer les liens `[[Prénom Nom]]` vers les fiches People
- Créer les fiches People manquantes AVANT d'archiver le meeting
- Ne pas copier le transcript complet — extraire les points pertinents
- Le lien Fireflies permet de retrouver le transcript complet si besoin
- Ne jamais dupliquer un meeting déjà archivé

---

## Recherche de meetings pour un projet

**Quand l'utilisateur demande de récupérer les meetings d'un projet :**

1. **Lire l'index du projet** pour identifier :
   - Les mots-clés du projet
   - Les parties prenantes (People)
   - Les entreprises impliquées

2. **Rechercher dans Fireflies** par :
   - Nom du projet / mots-clés
   - Noms des parties prenantes
   - Emails des participants (si connus)
   - Termes métier spécifiques (ex: "licitation", "SARL", etc.)

3. **Vérifier les doublons** :
   - Lister les meetings déjà archivés (`Glob _meetings/*.md`)
   - Comparer par date et participants
   - Ne pas re-archiver un meeting existant

4. **Archiver les nouveaux meetings pertinents** :
   - Suivre le format ci-dessus
   - Mettre à jour l'index du projet (section "Meetings clés")

**Exemple de recherche complète :**
```
# Projet "Les Jaunets" avec parties prenantes :
# Thérèse Dessauce, Cyrgue Dessauce, Adeline Pithois-Guillou, etc.

1. fireflies_search: keyword:"Jaunets"
2. fireflies_search: keyword:"Thérèse"
3. fireflies_search: keyword:"Cyrgue"
4. fireflies_search: keyword:"licitation"
5. fireflies_search: keyword:"notaire"
... etc pour chaque partie prenante et mot-clé métier
```

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (Fireflies webhooks)
- [x] Polling API (list meetings avec date filter)
- [ ] Sync manuelle uniquement

**Fireflies Webhooks :**
```bash
# Configurer dans Fireflies Dashboard → Integrations → Webhooks
# URL: https://your-domain.com/webhook/fireflies

# Payload reçu
{
  "meetingId": "xxx",
  "title": "Team Meeting",
  "date": "2024-07-15T10:00:00Z",
  "duration": 3600,
  "transcript_url": "https://app.fireflies.ai/view/xxx"
}
```

**Events Fireflies :**
- `transcription.complete` — Transcript prêt
- `meeting.processed` — Meeting traité
- `summary.ready` — Résumé disponible

**Polling API :**
```graphql
query {
  transcripts(
    fromDate: "2024-07-15"
    toDate: "2024-07-20"
  ) {
    id
    title
    date
    duration
  }
}
```

**Otter.ai :**
- Webhooks disponibles dans les plans Business
- Polling via API REST

**Setup requis :**
1. Configurer webhook dans Fireflies Dashboard
2. Ou script polling avec date filter
3. Stocker le dernier ID/date synchronisé

**Fréquence recommandée :**
- Webhooks : temps réel (quelques minutes après meeting)
- Polling : toutes les 30-60 minutes

---

## Notes

_Les configurations spécifiques (Fireflies, Otter, etc.) sont dans `local/TOOLS.md`._
