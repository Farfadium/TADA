---
A quoi sert ce fichier:
Système de gestion des tâches — Convention pour créer, suivre et rappeler les tâches dans DATA/
---

# Système de Tâches

> Les tâches vivent avec leur contexte, pas dans une liste déconnectée.

## Principe fondamental

**Une tâche appartient à son répertoire.**

Que ce soit un projet dans NOW/, un track, un dossier dans ARCHIVE/, ou n'importe où dans DATA/ — la tâche est créée là où elle a du sens.

Un index central (`DATA/TASKS-INDEX.md`) consolide tout automatiquement.

## Convention : fichier TASKS.md

N'importe quel répertoire dans DATA/ peut avoir un fichier `TASKS.md` :

```markdown
# Tâches — [Nom du contexte]

## En cours
- [ ] Description de la tâche @due(YYYY-MM-DD) @remind(YYYY-MM-DD)
- [ ] Autre tâche sans date

## En attente
- [ ] Tâche bloquée (raison)

## Fait
- [x] Tâche terminée @done(YYYY-MM-DD)
```

### Annotations supportées

| Annotation | Signification | Exemple |
|------------|---------------|---------|
| `@id(slug)` | Identifiant unique pour liens | `@id(banque-bnp)` |
| `@due(date)` | Date limite | `@due(2025-02-15)` |
| `@remind(date)` | Date de rappel | `@remind(2025-02-10)` |
| `@done(date)` | Date de complétion | `@done(2025-01-30)` |
| `@priority(high\|medium\|low)` | Priorité | `@priority(high)` |
| `@waiting(raison)` | En attente de quelqu'un/quelque chose | `@waiting(réponse notaire)` |

### Liens vers des tâches spécifiques

Les tâches avec `@id(slug)` peuvent être référencées depuis n'importe quel fichier :

```markdown
<!-- Dans TASKS.md -->
- [ ] Relancer BNP pour le prêt @id(banque-bnp) @due(2025-02-03)

<!-- Depuis un autre fichier (README, track, etc.) -->
Voir [relance banque](../TASKS.md#banque-bnp) pour le suivi.
```

**Quand utiliser @id :**
- Tâches importantes référencées ailleurs
- Tâches de coordination entre plusieurs contextes
- Tâches à suivre sur la durée

**Pas besoin d'@id :**
- Tâches simples locales au contexte
- Items de checklist (courses, etc.)

### Sections recommandées

- **En cours** : Tâches actives
- **En attente** : Bloquées par un facteur externe
- **Fait** : Historique (garder les 30 derniers jours, puis archiver)

## Index global : TASKS-INDEX.md

Fichier `DATA/TASKS-INDEX.md` — Vue consolidée de toutes les tâches actives.

**Généré automatiquement** par l'agent lors des heartbeats ou sur demande.

Format :
```markdown
# Index des Tâches

_Dernière mise à jour : YYYY-MM-DD HH:MM_

## À faire aujourd'hui
- [ ] Tâche urgente — [Projet](chemin/TASKS.md)

## Cette semaine
- [ ] Tâche avec deadline — [Contexte](chemin/TASKS.md) @due(date)

## Rappels à venir
| Date | Tâche | Contexte |
|------|-------|----------|
| 2025-02-01 | Relancer banque | [Jaunets](NOW/Les%20Jaunets/TASKS.md) |

## Par contexte
### NOW/Projet1
- [ ] Tâche 1
- [ ] Tâche 2

### ARCHIVE/Admin/Impots
- [ ] Tâche admin
```

## Intégration avec les rappels Moltbot

Quand une tâche a un `@remind(date)` :
1. L'agent crée un cron Moltbot pour cette date
2. Le rappel contient un lien vers la tâche : "📋 Rappel : [Tâche] → voir [contexte/TASKS.md]"
3. Quand le rappel se déclenche, l'agent peut retrouver le contexte complet

**Les crons Moltbot sont des triggers, pas la source de vérité.**
La source de vérité = les fichiers TASKS.md dans DATA/.

## Maintenance

### Lors des heartbeats
- Vérifier les tâches avec `@due` dans les 7 prochains jours
- Mettre à jour TASKS-INDEX.md si des changements
- Créer les rappels Moltbot pour les nouveaux `@remind`

### Hebdomadaire
- Nettoyer les tâches `@done` de plus de 30 jours
- Vérifier les tâches en attente prolongée

## Commandes vocales / texte

L'utilisateur peut dire :
- "Ajoute une tâche : relancer la banque pour les Jaunets, rappel lundi"
  → Crée dans `NOW/Les Jaunets/TASKS.md` + cron Moltbot
  
- "Quelles sont mes tâches ?"
  → Lit TASKS-INDEX.md, résume les priorités

- "Marque comme fait : relancer la banque"
  → Trouve la tâche, ajoute `@done(aujourd'hui)`, déplace en "Fait"

---

*Ce système remplace les rappels orphelins par des tâches contextualisées.*
