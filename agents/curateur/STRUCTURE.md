# PROPOSAL-YVAN.md — Proposition de structure TADA

**Utilisateur** : Yvan Wibaux
**Date** : 2026-01-31
**Basé sur** : Analyse de DATA/PENDING/ (57K fichiers)

---

## Profil déduit des données

**Yvan Wibaux** :
- **Entrepreneur** : Cofondateur d'Evaneos (voyage sur-mesure)
- **Dirigeant** : Sidekicks (accompagnement de leaders/dirigeants)
- **Conseiller** : Missions de conseil stratégique (Déclic CNV, etc.)
- **Investisseur** : Portfolio personnel (startups, immobilier)
- **Père de famille** : Fils Romain, projets immobiliers familiaux

**Activité principale actuelle** : Sidekicks (626 mentions dans 1630 meetings Fireflies)

---

## Données disponibles

| Source | Volume | Période |
|--------|--------|---------|
| Fireflies | 1,630 transcripts | 2021 → 2026 |
| Folk CRM | 300 contacts | - |
| Miro | 213 boards | 2020 → 2026 |
| Calendar | 50,000+ events | 2024 → 2026 |
| Emails | 12,500+ fichiers | 2022 → 2026 |

**Groupes Folk identifiés** :
- Holivia
- Leaders accompagnés
- Leads Sidekicks
- Leads

---

## Proposition de structure

### NOW/ — Ce qui est vivant

```
NOW/
├── index.md
│
├── Sidekicks/                 # Activité principale
│   ├── index.md
│   ├── Clients/               # Missions en cours
│   ├── Sales/                 # Pipeline commercial
│   ├── Équipe/                # Collaborateurs, associés
│   └── Produit/               # Méthode, formations
│
├── Evaneos/                   # Participation cofondateur
│   ├── index.md
│   ├── Opération-2026/        # Vente/restructuration en cours
│   └── Hodis/                 # Acquisition récente
│
├── Déclic-CNV/                # Mission conseil active
│   └── index.md
│
├── Les-Jaunets/               # Projet immobilier familial
│   ├── index.md
│   ├── _track_banques.md
│   ├── _track_travaux.md
│   └── _track_juridique.md
│
├── Investissements/           # Portfolio actif
│   ├── index.md
│   └── [Startup-X/]           # Un sous-dossier par investissement actif
│
└── TADA/                      # Ce projet (meta)
    ├── index.md
    ├── PROJECT/
    └── WEB/
```

**Logique** : Chaque dossier = quelque chose qui demande de l'énergie, de l'attention active.

**Note** : Famille n'est PAS dans NOW/. La vie familiale est stable, elle va dans ARCHIVE/. Seuls les *projets* familiaux spécifiques (choix d'école, déménagement...) vont dans NOW/ le temps qu'ils sont actifs.

---

### ARCHIVE/ — Tout le reste

**Premier niveau simple** : pas de hiérarchie complexe.

```
ARCHIVE/
├── index.md
│
├── Répertoires/               # === ANNUAIRES ===
│   ├── People/                # Personnes physiques (FLAT)
│   │   ├── index.md
│   │   └── [Prénom_Nom.md]    # Tout à plat, pas de sous-dossiers
│   │
│   └── Orgs/                  # Organisations (FLAT)
│       ├── index.md
│       └── [Nom_Org.md]       # Tout à plat, catégorisation par tags
│
├── Famille/                   # Vie familiale (stable, pas de "projet")
│   ├── index.md
│   ├── Romain/
│   └── [Autres membres]
│
├── Projets/                   # Projets terminés
│   ├── index.md
│   └── [Projet-terminé/]
│
├── Identité/                  # Documents personnels
│   ├── index.md
│   ├── Pièces/
│   ├── Diplômes/
│   └── Certifications/
│
├── Administratif/             # Structure légale et admin
│   ├── index.md
│   ├── Patrimoine/
│   ├── Immobilier/
│   ├── Banque/
│   ├── Fiscalité/
│   └── Entreprises/
│
├── Emails/                    # Historique par année
│   └── [YYYY/]
│
├── Meetings/                  # Transcripts par année
│   └── [YYYY/]
│
└── Boards/                    # Miro archivés
    └── index.md
```

---

## Annuaires proposés

### 1. People/ — Personnes physiques

**Pertinence** : ⭐⭐⭐⭐⭐ (300 contacts, mentions dans tous les meetings)

**Structure** : FLAT (pas de sous-dossiers). Catégorisation par tags.

**Structure d'une fiche** :
```markdown
# Prénom Nom

**Email** : ...
**Téléphone** : ...
**Entreprise** : [[Orgs/Nom]]
**Rôle** : ...

## Pourquoi cette fiche existe
(D'où vient ce contact ? Pourquoi est-il dans mon annuaire ? Quelle est ma relation personnelle avec cette personne ?)

## Contexte
(Comment je connais cette personne, histoire de la relation)

## Projets liés
- [[NOW/Sidekicks]] — Client depuis 2024
- [[NOW/Déclic-CNV]] — Contact via Karen

## Dernières interactions
- 2026-01-28 : Meeting "Karen Yvan"
- 2026-01-15 : Email "Re: Proposition"

## Tags
#client-sidekicks #lead #partenaire #famille #ami
```

**Catégorisation** : Par tags (une personne peut être ami ET partenaire business)

---

### 2. Orgs/ — Organisations

**Pertinence** : ⭐⭐⭐⭐ (beaucoup d'entreprises dans les emails/meetings)

**Structure** : FLAT (pas de sous-dossiers). Catégorisation par tags/métadonnées.

**Structure d'une fiche** :
```markdown
# Nom de l'Entreprise

**Type** : Client | Partenaire | Investissement | Fournisseur
**Site** : https://...
**Secteur** : ...

## Pourquoi cette fiche existe
(Contexte personnel : comment je connais cette org, pourquoi elle est importante pour moi)

## Contacts
- [[People/Prénom_Nom]] — CEO
- [[People/Autre_Contact]] — DRH

## Relation
(Nature de la relation avec Yvan)

## Projets liés
- [[NOW/Sidekicks]] — Client depuis 2024

## Historique
- 2025-03 : Premier contact
- 2025-06 : Signature contrat

## Tags
#client #sidekicks #tech #paris
```

**Catégorisation** : Par tags dans les fichiers, pas par sous-dossiers.

---

### 3. Pas d'annuaire "Lieux"

**Justification** : Les lieux importants (Batz-sur-Mer, Les Jaunets) sont déjà dans NOW/ ou ARCHIVE/Administratif/Immobilier/. Pas assez de lieux distincts pour justifier un annuaire.

---

### 4. Pas d'annuaire "Thèmes"

**Justification** : Les thèmes (CNV, leadership, investissement) sont mieux gérés par tags dans les fichiers. Un dossier "Thèmes" créerait de la redondance.

---

## ⚠️ Règle critique : Personnalisation des annuaires

**Chaque entrée d'annuaire doit être personnalisée.**

Ce ne sont PAS des fiches génériques copiées d'un CRM. Chaque fiche doit répondre à :

1. **Pourquoi cette entrée existe** — D'où vient-elle ? Quel événement a créé cette fiche ?
2. **Quelle est ma relation** — Comment JE connais cette personne/org ? Pas une bio Wikipedia.
3. **Pourquoi c'est pertinent pour MOI** — En quoi cette entrée m'est utile ?

**Exemple mauvais** :
```markdown
# Acme Corp
Site : https://acme.com
Secteur : Tech
```

**Exemple bon** :
```markdown
# Acme Corp
Site : https://acme.com

## Pourquoi cette fiche existe
Rencontré via Nicolas au Web Summit 2024. Discussion sur un partenariat potentiel pour Sidekicks.

## Ma relation
Contact initial avec [[People/Jean_Dupont]] (CEO). Échange de 3 emails en novembre 2024, pas de suite pour l'instant.

## Statut
En veille. À recontacter si opportunité pertinente.
```

**Les annuaires sont une base de données personnelle, pas un annuaire public.**

---

## Règles de liens

### Quand créer une fiche People/ ?

- ✅ Personne avec qui Yvan a eu ≥ 2 interactions
- ✅ Contact important (client, partenaire clé, famille)
- ❌ Email unique sans suite (newsletter sender, spam)
- ❌ Participant passif à un meeting de groupe

### Quand créer une fiche Orgs/ ?

- ✅ Entreprise avec relation business (client, partenaire, investissement)
- ✅ Organisation avec ≥ 2 contacts connus
- ❌ Entreprise mentionnée une fois en passant
- ❌ Fournisseur ponctuel (hôtel, restaurant)

### Bidirectionnalité

Quand un fichier mentionne une entité :
1. Ajouter `[[People/X]]` ou `[[Orgs/X]]` dans le fichier
2. Ajouter un backlink dans la fiche de l'annuaire

---

## Alternatives considérées

### Option A : Annuaires dans ARCHIVE/ (recommandée ✓)

```
ARCHIVE/Répertoires/People/
ARCHIVE/Répertoires/Orgs/
```

**Avantage** : Les annuaires sont des références stables, pas des éléments "vivants".

### Option B : Annuaires à la racine de DATA/

```
DATA/People/
DATA/Orgs/
```

**Avantage** : Accès plus direct, même niveau que NOW/ et ARCHIVE/.
**Inconvénient** : Mélange la logique NOW/ARCHIVE avec les annuaires.

### Option C : Annuaires dans un dossier dédié

```
DATA/INDEX/People/
DATA/INDEX/Orgs/
```

**Avantage** : Séparation claire.
**Inconvénient** : Crée un 3ème concept en plus de NOW/ARCHIVE.

---

## Décisions validées ✅

| Question | Décision |
|----------|----------|
| NOW/Famille/ | ❌ Non. Famille → ARCHIVE/. Seuls les projets ponctuels (choix école...) vont dans NOW/. |
| Où mettre les annuaires | ✅ ARCHIVE/Répertoires/. Premier niveau simple. |
| Orgs/ : structure | ✅ FLAT. Pas de sous-dossiers, catégorisation par tags. |
| Historique emails | ✅ Garder la plupart. Supprimer seulement les emails vides (accusés de réception, confirmations). Classer le reste. |
| Personnalisation annuaires | ✅ Chaque fiche doit expliquer pourquoi elle existe, d'où elle vient, quelle relation personnelle. |

## Questions restantes

1. **Projets Sidekicks** — Un sous-dossier par client/mission dans NOW/Sidekicks/, ou juste des références vers les fiches Orgs/ ?

---

## Prochaines étapes

Si cette structure est validée :

1. **Créer les dossiers** vides avec leurs index.md
2. **Peupler People/** à partir de Folk + déduplication
3. **Peupler Orgs/** à partir des entreprises identifiées
4. **Classifier les emails** → NOW/ ou ARCHIVE/Emails/
5. **Classifier les meetings** → NOW/ ou ARCHIVE/Meetings/
6. **Enrichir NOW/** avec les données liées

---

*Ce document est une proposition. L'utilisateur doit valider avant toute action.*
