## Index

**Ton rôle clé : maintenir les index à jour.**

À chaque information reçue (email, fichier, conversation), tu mets à jour les index concernés :
- Nouveau fichier → ajouter dans la liste des fichiers
- Nouvelle info sur un projet → mettre à jour le statut, les tâches, les notes
- Nouveau contact → ajouter dans les parties prenantes
- Décision prise → mettre à jour le statut

**Tu ne laisses jamais un index devenir obsolète.**

---

Tu documentes chaque dossier avec un fichier `index.md`.

**Quand tu crées ou modifies un projet, tu utilises ce template :**

```markdown
# Nom du projet
> Description courte

## Objectif
## Enjeux
## Parties prenantes
## Budget & Planning
---
## Statut
## À faire
## Questions
---
## Structure des dossiers
## Fichiers
## Notes
```

**Mots-clés — tu les identifies :**
Chaque projet a des mots-clés uniques pour le routage automatique :
- Noms de personnes
- Sociétés
- Lieux
- Codes projet

Tu utilises ces mots-clés pour router automatiquement les emails et fichiers.

**Documents partagés :**
Certains documents sont utilisés par plusieurs projets (ex: avis d'imposition pour dossiers bancaires).
- **Stockage** : `DATA/ARCHIVE/Administratif/[Catégorie]/` (ex: Impôts/, Identité/, Banques/)
- **Dans les projets** : créer un lien relatif vers le document
- **Exemple** : `[Avis d'imposition](../../ARCHIVE/Administratif/Impôts/2025_Avis_imposition.pdf)`

Tu évites de dupliquer les documents. Un seul exemplaire, plusieurs liens.

**Template ARCHIVE — pour les dossiers de consultation :**
```markdown
# Nom du dossier

Description en une ligne.

## Contenu
| Dossier | Documents |
```

**Template INVESTISSEMENT — pour les participations :**
```markdown
# Nom de l'entreprise

Description activité.

## Informations clés
- Date d'investissement
- Montant investi
- Nombre d'actions / %
- Prix par action
- Véhicule

## Évolution du capital
| Date | Événement | Valorisation |

## Stratégie
## Statut actuel
## Documents disponibles
```

---

## Tracks

**Quand utiliser des tracks :**
Les projets complexes ont souvent plusieurs axes de travail parallèles (financement, travaux, juridique, etc.). Plutôt que de tout mettre dans l'index, on crée un fichier par track.

**Avantages :**
- Index reste synthétique (vue d'ensemble)
- Chaque track a son historique détaillé
- Plusieurs tracks peuvent avancer en parallèle
- Facilite le suivi granulaire

**Convention de nommage :** `_track_[nom].md`

**Template TRACK :**
```markdown
# Track [Nom]

> [Description courte du track]

## Objectif
[Ce qu'on cherche à obtenir sur ce track]

## Interlocuteurs
| Entité | Contact | Rôle |
|--------|---------|------|
| [[Entreprise]] | [[Prénom Nom]] | Description |

## Suivi
| Date | Action | Résultat | Prochaine étape |
|------|--------|----------|-----------------|
| JJ/MM | Description | ✅/🟡/❌ | Action suivante |

## Statut actuel
🟢 En bonne voie / 🟡 En attente / 🔴 Bloqué / ⚪ Non démarré

**Dernière action :** [Date] — [Description]
**Prochaine étape :** [Action attendue]

## Historique détaillé

### [Date] — [Titre]
[Description de l'événement, décisions, échanges]

---

## Documents
- [Document](chemin) — description

## Notes
```

**Dans l'index du projet :**
Ajouter une section "Tracks" avec le nom cliquable :
```markdown
## Tracks
| Track | Statut | Prochaine étape |
|-------|--------|-----------------|
| [Banques](_track_banques.md) | 🟡 En attente | Action à faire |
| [Travaux](_track_travaux.md) | 🟢 En cours | Action à faire |
```
