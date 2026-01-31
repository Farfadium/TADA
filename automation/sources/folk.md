---
description: Configuration source Folk CRM — sync contacts, notes, enrichissement fiches People, suivi relations
---

### Folk

> CRM personnel — contacts, notes, suivi relations.

**Type :** `crm`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**API disponible :** Folk API (developer.folk.app)

**Formats d'export :**
- CSV : contacts (via UI ou API)
- CSV : notes associées aux contacts
- ZIP : contacts.csv + notes.csv

**Prérequis :**
- Plan Premium ou Custom (pour accès API)
- API key générée depuis Folk

**Accès :**
- [x] Lecture (contacts, notes)
- [x] Écriture (création/update contacts via API)
- [ ] Suppression (jamais automatique)

---

## Comportement

**Ce que l'IA peut faire :**
- Lire les contacts et leurs données
- Récupérer les notes associées
- Enrichir les fiches `People/` avec les données Folk
- Synchroniser les contacts entre Folk et TADA
- Créer/mettre à jour des contacts dans Folk

**Ce que l'IA ne fait JAMAIS :**
- Supprimer un contact sans confirmation
- Partager des données de contacts avec des tiers
- Modifier des informations sans validation
- Exfiltrer des données sensibles

**Règles spécifiques :**
- Folk est la source de vérité pour les contacts professionnels
- Les fiches `People/` sont enrichies avec les données Folk
- Synchronisation bidirectionnelle : TADA ↔ Folk
- Toujours vérifier les doublons avant d'importer

---

## Sync

**Fréquence :** `session` (à chaque démarrage) ou `quotidien`

**Critères de récupération :**
- Tous les contacts actifs
- Notes modifiées depuis dernière sync
- Nouveaux contacts créés

**Workflow :**
1. Export CSV depuis Folk (ou API call)
2. Import dans TADA
3. Matching avec fiches `People/` existantes
4. Mise à jour ou création de fiches

---

## Actions sync

À chaque sync, l'IA :
1. Récupère les contacts depuis Folk (CSV ou API)
2. Pour chaque contact :
   - Cherche une fiche correspondante dans `DATA/ARCHIVE/Répertoires/People/`
   - Si fiche existe → comparer et proposer mise à jour si différences
   - Si fiche n'existe pas → créer la fiche avec données Folk
3. Récupère les notes associées
4. Enrichit les fiches avec les notes pertinentes
5. Affiche : "👥 X contacts synchronisés" + résumé des changements

---

## Enrichissement des fiches People

**Données à synchroniser depuis Folk :**
- Nom complet
- Email(s)
- Téléphone(s)
- Entreprise actuelle
- Poste
- LinkedIn
- Tags/labels Folk
- Notes importantes
- Dernière interaction

**Format de la fiche People enrichie :**
```markdown
---
nom: Prénom Nom
entreprise: [[Entreprise]]
poste: Titre du poste
email: email@exemple.com
telephone: +33 X XX XX XX XX
linkedin: https://linkedin.com/in/xxx
tags: [tag1, tag2, tag3]
source: Folk
derniere_maj: YYYY-MM-DD
---

# Prénom Nom

## Infos

- **Entreprise :** [[Entreprise]]
- **Poste :** Titre du poste
- **Email :** email@exemple.com
- **Téléphone :** +33 X XX XX XX XX
- **LinkedIn :** [Profil](https://linkedin.com/in/xxx)

## Notes Folk

[Notes importantes synchronisées depuis Folk]

## Historique interactions

- YYYY-MM-DD : [type d'interaction]

## Liens projets

- [[Projet 1]]
- [[Projet 2]]
```

**Règles de synchronisation :**
- Ne jamais écraser des notes manuscrites dans TADA
- Ajouter les notes Folk dans une section dédiée
- Garder la traçabilité : indiquer la source (Folk) et date de sync
- En cas de conflit : proposer à l'utilisateur de choisir

---

## Export Folk → TADA

**Méthode 1 : Export CSV manuel**
1. Dans Folk : Export → Download CSV
2. Obtenir `contacts.csv` + `notes.csv` dans un ZIP
3. Upload du ZIP dans TADA
4. L'IA parse les CSV et crée/met à jour les fiches

**Méthode 2 : API (si disponible)**
1. Appel API pour récupérer tous les contacts
2. Appel API pour récupérer les notes
3. Traitement automatique et mise à jour des fiches

---

## Import TADA → Folk

**Quand créer des contacts dans Folk :**
- Nouvelle personne rencontrée (meeting, email, etc.)
- Contact important pour un projet
- Personne à suivre dans le temps

**Workflow :**
1. Fiche créée dans `People/` via une conversation/meeting/email
2. L'IA propose : "Ajouter ce contact dans Folk ?"
3. Si oui → création via API ou export CSV pour import manuel

---

## Archivage des interactions

**Les notes Folk peuvent être archivées dans les projets :**

Si une note Folk concerne un projet spécifique :
- Créer un fichier dans `DATA/NOW/[Projet]/_interactions/YYYY-MM-DD_Prénom-Nom.md`
- Lier vers la fiche `[[Prénom Nom]]`
- Copier la note pertinente depuis Folk

**Format :**
```markdown
# Interaction avec [[Prénom Nom]]

- **Date :** YYYY-MM-DD
- **Type :** Call / Meeting / Email
- **Projet :** [[Nom du projet]]
- **Source :** Folk CRM

## Notes

[Notes copiées depuis Folk]

## Actions

- [ ] Action item 1
- [ ] Action item 2
```

---

## Recherche de contacts pour un projet

**Quand l'utilisateur demande "Qui sont les contacts sur ce projet ?" :**

1. **Lire l'index du projet** pour identifier :
   - Les parties prenantes mentionnées
   - Les entreprises impliquées

2. **Chercher dans Folk** (via API ou CSV) :
   - Par tags/labels liés au projet
   - Par entreprise
   - Par nom des personnes

3. **Lister les contacts pertinents** :
   - Vérifier s'ils ont une fiche dans `People/`
   - Proposer de créer les fiches manquantes

---

## Notes

**Folk vs People/ :**
- Folk = CRM actif, contacts en cours
- People/ = Mémoire long-terme TADA avec contexte enrichi
- Synchronisation = garder les deux à jour

**Règles de fusion :**
- Folk a priorité pour : email, téléphone, poste, entreprise (données "officielles")
- TADA a priorité pour : notes contextuelles, liens projets, historique détaillé

---

## Détection nouvelles données

**Méthode disponible :**
- [x] Webhook/Push (Folk webhooks)
- [x] Polling API (avec pagination)
- [ ] Sync manuelle uniquement

**Folk Webhooks :**
```bash
# Configurer dans Folk → Settings → Integrations → Webhooks
# URL: https://your-domain.com/webhook/folk

# Events disponibles
- contact.created
- contact.updated
- contact.deleted
- note.created
- note.updated
```

**Polling API :**
```bash
# Récupérer les contacts modifiés
curl "https://api.folk.app/v1/contacts?updated_since=2024-07-15T00:00:00Z" \
  -H "Authorization: Bearer $FOLK_API_KEY"
```

**Setup requis :**
1. Créer un webhook dans Folk Dashboard
2. Ou configurer polling régulier
3. Stocker le dernier timestamp de sync

**Fréquence recommandée :**
- Webhooks : temps réel
- Polling : toutes les 30 minutes à 1 heure

_Les configurations spécifiques (API key, compte, etc.) sont dans `local/TOOLS.md`._