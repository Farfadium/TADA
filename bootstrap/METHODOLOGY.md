# METHODOLOGY.md — Bootstrap TADA from PENDING

**Objectif** : Transformer un dépôt brut de données (`DATA/PENDING/`) en un TADA structuré et vivant.

---

## Contexte

L'utilisateur a collecté toutes ses données disponibles :
- Emails (exports ou API)
- Contacts (CRM, carnet d'adresses)
- Calendrier (events passés et futurs)
- Meetings (transcripts, notes)
- Fichiers divers (documents, captures, audio)
- Boards/notes (Miro, Notion, etc.)

Tout est déversé dans `DATA/PENDING/`. L'agent doit créer la structure TADA à partir de ce chaos.

---

## Principes fondamentaux

### 1. NOW/ = Ce qui est vivant

`NOW/` contient tout ce qui a une existence active aujourd'hui :
- Projets en cours
- Activités récurrentes
- Entreprises où l'utilisateur est impliqué
- Relations actives importantes
- Sujets d'attention actuels

**Ce n'est PAS** une liste de "projets" au sens strict. C'est la réponse à : "Sur quoi tu travailles / vis en ce moment ?"

### 2. ARCHIVE/ = Tout ce qui n'est pas vivant mais utile

`ARCHIVE/` contient **tout ce dont on a besoin** mais qui n'est pas actif :

- **Projets terminés** — anciens projets, missions closes
- **Annuaires/Répertoires** — People, Orgs, et autres index de référence
- **Identité** — documents personnels, pièces d'identité, certifications
- **Administratif** — statuts, contrats, documents de structure
- **Historique** — emails anciens, meetings passés, archives thématiques

**ARCHIVE/ a sa propre structure** qui doit être pensée avec autant de soin que NOW/.

### 3. Les annuaires = Index transversaux

Les annuaires sont des **répertoires de référence** qui permettent de retrouver des entités qui traversent plusieurs éléments.

**Important** : Avant de créer un annuaire, se demander :
- Quel type d'entités est pertinent pour cet utilisateur ?
- Quels annuaires seront réellement utiles ?
- Comment les nommer et les structurer ?

---

## Méthodologie de tri

### Phase 0 : Conception de la structure

**AVANT de commencer à trier**, réfléchir à la structure cible.

#### 0.1 Définir les annuaires pertinents

Analyser les données dans PENDING/ et identifier quels types d'entités émergent :

| Question | Décision |
|----------|----------|
| Y a-t-il beaucoup de personnes ? | → Créer `People/` |
| Y a-t-il des entreprises/organisations ? | → Créer `Orgs/` |
| Y a-t-il des lieux importants ? | → Créer `Lieux/` ? |
| Y a-t-il des thèmes transversaux ? | → Tags ou dossiers ? |

**Ne pas créer d'annuaire "au cas où"** — seulement ceux qui seront réellement peuplés et utilisés.

#### 0.2 Définir la structure de ARCHIVE/

Proposer une structure pour ARCHIVE/ adaptée aux données :

```
ARCHIVE/
├── People/              # Annuaire des personnes
├── Orgs/                # Annuaire des organisations
├── Projets/             # Projets terminés
├── Identite/            # Documents personnels
├── Administratif/       # Statuts, contrats, structure
├── Emails/              # Historique emails par année
│   ├── 2024/
│   └── 2025/
├── Meetings/            # Transcripts archivés
└── [Autres selon besoin]
```

#### 0.3 Définir la structure de NOW/

Identifier les éléments vivants qui méritent un dossier :

```
NOW/
├── Projet-A/
├── Activite-B/
├── Entreprise-C/
└── index.md
```

**Validation** : Présenter la structure proposée à l'utilisateur AVANT de commencer le tri.

---

### Phase 1 : Inventaire

1. **Lister les sources** présentes dans PENDING/
2. **Compter et catégoriser** (nombre, période, format)
3. **Créer un rapport** : `PENDING/INVENTORY.md`

---

### Phase 2 : Extraction des entités et création des annuaires

#### 2.1 Créer les annuaires (structures vides)

Créer les dossiers décidés en Phase 0 avec leur `index.md`.

#### 2.2 Peupler les annuaires

Pour chaque type d'entité :

**Personnes (People/)** :
1. Extraire toutes les personnes uniques
2. Dédupliquer
3. Créer un fichier par personne
4. **Mettre à jour TOUS les fichiers qui mentionnent cette personne** avec un lien `[[People/Prénom_Nom]]`

**Organisations (Orgs/)** :
1. Extraire les organisations uniques
2. Créer un fichier par org
3. **Mettre à jour TOUS les fichiers** qui mentionnent cette org avec un lien `[[Orgs/Nom_Org]]`

**Règle critique** : Quand une entité est ajoutée à un annuaire, **tous les fichiers existants** qui la mentionnent doivent être mis à jour pour inclure le lien vers l'entrée de l'annuaire.

---

### Phase 3 : Classification et déplacement

**"Rattacher" = DÉPLACER le fichier** au bon endroit, pas juste ajouter une référence.

#### 3.1 Éléments vivants → NOW/

Pour chaque cluster identifié comme "vivant" :
1. Créer le dossier dans NOW/
2. **Déplacer** les fichiers associés (emails, meetings, docs) dans ce dossier
3. Créer/mettre à jour l'index.md du dossier

#### 3.2 Éléments non-vivants → ARCHIVE/

Pour les fichiers qui ne sont pas "vivants" :
1. Identifier la catégorie ARCHIVE/ appropriée
2. **Déplacer** le fichier
3. S'assurer que les liens vers les annuaires sont en place

---

### Phase 4 : Maillage des liens

Une fois tous les fichiers déplacés :

1. **Vérifier** que chaque fichier contient des liens vers :
   - Les personnes mentionnées → `[[People/...]]`
   - Les organisations mentionnées → `[[Orgs/...]]`
   - Les projets/activités liés → `[[NOW/...]]` ou `[[ARCHIVE/...]]`

2. **Dans chaque fiche d'annuaire**, ajouter les backlinks :
   - Fiche personne → liste des projets où elle apparaît
   - Fiche org → liste des projets/emails liés

---

### Phase 5 : Nettoyage

1. **Vider PENDING/** — tout a été déplacé
2. **Documenter la structure** dans `DATA/index.md`
3. **Créer MEMORY.md** avec le contexte initial

---

## Structure type de ARCHIVE/

```
ARCHIVE/
├── index.md                 # Vue d'ensemble
│
├── People/                  # Annuaire personnes
│   ├── index.md
│   └── [Prénom_Nom.md ...]
│
├── Orgs/                    # Annuaire organisations
│   ├── index.md
│   └── [Nom_Org.md ...]
│
├── Projets/                 # Projets terminés
│   ├── index.md
│   └── [Nom-Projet/]
│
├── Identite/                # Documents personnels
│   ├── index.md
│   ├── Pieces-Identite/
│   ├── Diplomes/
│   └── Certifications/
│
├── Administratif/           # Structure légale/admin
│   ├── index.md
│   ├── Entreprises/         # Statuts, Kbis, etc.
│   ├── Immobilier/          # Actes, baux, etc.
│   └── Banque/              # Comptes, contrats
│
├── Emails/                  # Historique par année
│   ├── 2024/
│   └── 2025/
│
└── Meetings/                # Transcripts archivés
    └── YYYY/
```

Cette structure est un **exemple** — elle doit être adaptée aux données réelles de l'utilisateur.

---

## Algorithme de classification

Pour chaque fichier dans PENDING/ :

```
1. IDENTIFIER le type (email, meeting, document, contact...)

2. EXTRAIRE les entités mentionnées :
   - Personnes → créer/enrichir fiche People/
   - Organisations → créer/enrichir fiche Orgs/
   
3. POUR CHAQUE entité extraite :
   - Ajouter un lien [[Annuaire/Entité]] dans le fichier
   - Ajouter un backlink dans la fiche de l'annuaire

4. DÉCIDER de la destination :
   - Est-ce vivant/actif ? → NOW/[Dossier]/
   - Est-ce un document de référence ? → ARCHIVE/[Catégorie]/
   - Est-ce de l'historique daté ? → ARCHIVE/[Type]/YYYY/

5. DÉPLACER le fichier vers sa destination
```

---

## Règles de nommage

### Fichiers annuaires
`Prénom_Nom.md` ou `Nom_Organisation.md` (underscores, pas d'espaces)

### Dossiers NOW/
Nom court et descriptif, pas de dates :
- ✅ `Sidekicks/`
- ✅ `Renovation-Maison/`
- ❌ `Projet-2026-01-Sidekicks/`

### Dossiers ARCHIVE/
Catégories claires et stables :
- ✅ `Identite/`
- ✅ `Administratif/Immobilier/`
- ❌ `Vieux-Trucs/`

### Fichiers datés
`YYYY-MM-DD_Sujet_Court.md`

---

## Validation humaine

Points de validation **obligatoires** :

1. **Phase 0** : "Voici la structure que je propose. OK ?"
2. **Création d'annuaire** : "Je propose de créer un annuaire [X]. Pertinent ?"
3. **Création NOW/** : "Je propose de créer [X] dans NOW/ basé sur [Y]. OK ?"
4. **Cas ambigus** : "Ce fichier pourrait aller dans [A] ou [B]. Ton choix ?"

---

## Métriques de succès

À la fin du bootstrap :

- [ ] PENDING/ est vide
- [ ] La structure ARCHIVE/ est cohérente et documentée
- [ ] Les annuaires pertinents existent et sont peuplés
- [ ] NOW/ reflète ce qui est vivant aujourd'hui
- [ ] **Tous les liens croisés sont en place** (fichiers ↔ annuaires)
- [ ] L'utilisateur peut naviguer et retrouver l'info

---

## Notes pour l'agent

- **Structure d'abord** : Phase 0 avant tout. Ne pas trier sans plan.
- **Liens bidirectionnels** : Chaque lien vers un annuaire = backlink dans l'annuaire.
- **Déplacer, pas copier** : Un fichier = un emplacement. Pas de doublons.
- **Demande** : Mieux vaut une question que 100 mauvais classements.
- **Documente** : Note tes décisions dans un log.

---

*Ce document définit la méthodologie. L'exécution se fait par phases, avec validation utilisateur à chaque étape clé.*
