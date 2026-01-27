### Initialisation projet

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Tag | #init [nom du projet] |

**Contexte :**
Créer la structure complète d'un nouveau projet pour qu'il soit immédiatement opérationnel dans TADA.

**Actions :**

1. Demander les informations de base :
   - Nom du projet
   - Description courte
   - Objectif principal
   - Parties prenantes (personnes, entreprises)

2. Créer la structure :
   - Dossier `NOW/[Nom Projet]/`
   - Fichier `index.md` avec le template projet

3. Identifier les mots-clés de routage :
   - Noms des parties prenantes
   - Nom du projet et variantes
   - Codes ou références spécifiques

4. Configurer Gmail :
   - Créer le label correspondant au projet
   - Proposer un filtre si pertinent

5. Créer les fiches manquantes :
   - Vérifier si les personnes/entreprises existent dans les répertoires
   - Proposer de créer les fiches manquantes

**Validation requise :** Oui (à chaque étape)

**Exemple :**
```
#init Achat Maison Bordeaux

→ Questions :
1. Description : Achat résidence principale à Bordeaux
2. Objectif : Finaliser l'achat avant juin 2026
3. Parties prenantes : Notaire Dupont, Agence ImmoPlus, Banque CréditNord

→ Structure créée :
NOW/Achat Maison Bordeaux/
└── index.md

→ Mots-clés de routage :
- "Achat Maison Bordeaux"
- "Dupont" (notaire)
- "ImmoPlus"
- "CréditNord"

→ Gmail :
- Label créé : "Achat Maison Bordeaux"

→ Fiches à créer :
- [[Dupont]] (notaire) - créer ?
- [[ImmoPlus]] (agence) - créer ?
- [[CréditNord]] (banque) - existe déjà

Valider ?
```
