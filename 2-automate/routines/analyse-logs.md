### Analyse des logs

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Temps | Mensuel (1er du mois) |
| Tag | #analyse-logs |

**Objectif :**
Lire entre les lignes des conversations pour comprendre les besoins non exprimés, les frustrations, les intentions profondes — et proposer des améliorations du système TADA dans son ensemble.

**Emplacement des logs :** `_SYSTEM/local/Claude_logs/`

---

**Ce que je cherche :**

| Signal | Ce que ça révèle |
|--------|------------------|
| Questions répétées | Besoin de documentation ou de clarté |
| Hésitations, reformulations | Concept mal défini ou structure confuse |
| Micro-validations ("oui", "go") | Manque d'autonomie, trop de friction |
| Abandons de conversation | Frustration, mauvaise direction |
| Demandes de "faire comme avant" | Régression, changement non souhaité |
| Idées évoquées puis oubliées | Projets latents à capturer |
| Plaintes implicites | Pain points à résoudre |

---

**Actions :**

1. **Lire l'ensemble des conversations récentes**
   - Extraire les messages utilisateur
   - Noter le contexte et l'émotion derrière chaque échange

2. **Identifier les intentions profondes**
   - Qu'est-ce que l'utilisateur essayait vraiment de faire ?
   - Où le système l'a-t-il freiné ?
   - Quelles idées sont restées en suspens ?

3. **Détecter les frustrations**
   - Reformulations multiples = incompréhension
   - Réponses courtes = impatience
   - Abandon = échec du système

4. **Repérer les opportunités**
   - Tâches manuelles récurrentes → automatiser
   - Questions fréquentes → documenter
   - Idées évoquées → capturer dans GARDEN ou projets

5. **Proposer des améliorations TADA**
   - Structure des dossiers
   - Routines manquantes
   - Documentation à clarifier
   - Nouvelles fonctionnalités

---

**Format du rapport :** `_SYSTEM/local/analyse-logs.md`

```markdown
# Analyse des logs — [YYYY-MM-DD]

## Période analysée
- X conversations
- [date début] → [date fin]

## Ce que j'ai compris

### Tes priorités actuelles
- ...

### Ce qui te frustre
- ...

### Idées en suspens
- ...

## Améliorations proposées pour TADA

| Priorité | Proposition | Impact |
|----------|-------------|--------|
| 1 | ... | ... |

## Questions pour toi
- ...
```

---

**Validation requise :** Oui (pour toute modification du système)

**Exemple :**
```
#analyse-logs

J'ai lu les 19 conversations du mois...

---

## Ce que j'ai compris

### Tes priorités actuelles
- Finaliser la structure TADA pour pouvoir la partager
- Réduire la friction dans nos échanges

### Ce qui te frustre
- Trop de validations demandées pour des actions simples
- Pas assez clair comment le système fonctionne techniquement

### Idées en suspens
- Subagents pour les routines (évoqué mais pas implémenté)
- Template anonymisé pour partage

## Améliorations proposées

| Priorité | Proposition | Impact |
|----------|-------------|--------|
| 1 | Définir les actions sans validation | Moins de friction |
| 2 | Documenter le fonctionnement technique | Autonomie utilisateur |
| 3 | Créer routine export-template | Partage facilité |

## Questions pour toi
- Veux-tu que je puisse modifier les fichiers système sans demander ?
- Le rythme mensuel pour cette analyse te convient ?

Valider les propositions ?
```
