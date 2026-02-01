---
A quoi sert ce fichier:
Architecture multi-agents TADA — Définit les rôles, responsabilités et interactions entre agents spécialisés
---

# Architecture Multi-Agents TADA

> Une équipe d'agents spécialisés qui maintiennent le système en background.

## Pourquoi des agents multiples ?

Un seul agent qui fait tout mélange :
- Répondre aux questions
- Maintenir les sources
- Structurer les données
- Coder le système

Ça crée du bruit et du mélange de contexte. La solution : **spécialisation**.

---

## Les Agents Core

### 🎯 Agent Principal — "Cassiopée"

**Rôle :** Interface avec l'utilisateur, chef d'orchestre.

**Responsabilités :**
- Répond aux questions et demandes
- Délègue aux agents spécialisés
- Coordonne les actions complexes
- Synthétise les rapports des autres agents

**Runtime :** Session principale (Moltbot/Claude Code)

---

### 🔌 Agent Sources — "Collecteur"

**Rôle :** La donnée rentre correctement.

**Responsabilités :**
- Vérifie que toutes les sources sont connectées
- Détecte les sources cassées (API expirée, auth échouée)
- Lance les syncs régulières
- Propose de nouvelles sources à connecter
- Rapport : "X nouveaux emails, Y meetings, source Z en erreur"

**Fichiers surveillés :**
- `_SYSTEM/2-Automate/sources/`
- `_SYSTEM/runtimes/*/TOOLS.md`

**Déclencheur :** Cron quotidien ou heartbeat dédié

---

### 🗂️ Agent Structure — "Curateur"

**Rôle :** TADA est propre et navigable.

**Implémentation :** [`_SYSTEM/agents/curateur/`](../agents/curateur/)

**Responsabilités :**
- Vérifie la cohérence de la structure DATA/
- Détecte les dossiers trop gros → propose split
- Détecte les projets inactifs → propose archivage
- Maintient les liens entre fichiers
- Vérifie les fiches People/Orgs à jour
- Rapport : "Projet X inactif depuis 3 mois, 45 fichiers sans liens"

**Fichiers surveillés :**
- `DATA/` (toute l'arborescence)
- `DATA/PENDING/` (durée de vie des fichiers)

**Déclencheur :** Cron hebdomadaire

---

### 🔧 Agent Système — "Tech Lead"

**Rôle :** _SYSTEM fonctionne et évolue.

**Responsabilités :**
- Relit les conversations pour capturer les décisions
- Met à jour la documentation quand nécessaire
- Vérifie la cohérence entre runtimes
- Propose des améliorations au système
- Teste les nouveaux composants
- Maintient CONTRIBUTING.md à jour

**Fichiers surveillés :**
- `_SYSTEM/` (toute la documentation)
- Logs de conversation (pour extraction de décisions)

**Déclencheur :** Après sessions importantes ou cron hebdomadaire

---

### 📝 Agent Mémoire — "Scribe"

**Rôle :** Le contexte est préservé.

**Responsabilités :**
- Met à jour `MEMORY.md` (mémoire long-terme)
- Crée les daily notes (`DATA/memory/YYYY-MM-DD.md`)
- Capture les décisions importantes
- Maintient le contexte entre sessions
- Nettoie les notes > 90 jours

**Fichiers surveillés :**
- `MEMORY.md`
- `DATA/memory/`

**Déclencheur :** Fin de session ou heartbeat

---

## Agents Optionnels

| Agent | Rôle | Déclencheur |
|-------|------|-------------|
| **Veilleur** | Surveille sources externes (news, RSS, mentions) | Cron |
| **Financier** | Suit les investissements, alertes variations | Cron + seuils |
| **Relationnel** | Rappelle follow-ups, anniversaires, relances | Cron quotidien |
| **Rédacteur** | Prépare drafts, résumés, synthèses | À la demande |

---

## Architecture

```
Utilisateur
    ↓
🎯 TADA (Principal)
    ↓
┌───────┴───────┬─────────────┬────────────┐
↓               ↓             ↓            ↓
🔌 Collecteur   🗂️ Archiviste  🔧 Tech Lead  📝 Scribe
(sources)       (structure)   (système)    (mémoire)
```

**Principes :**
- Chaque agent a son scope défini
- Ils travaillent en background (cron/heartbeat)
- Ils reportent au principal (ou directement à l'utilisateur si urgent)
- Ils ont accès aux mêmes fichiers mais des responsabilités différentes
- Pas de duplication de travail

---

## Implémentation

### Option 1 : Heartbeats différenciés

Un seul agent avec des "modes" selon le heartbeat :
```
HEARTBEAT_COLLECTEUR → vérifie sources
HEARTBEAT_ARCHIVISTE → vérifie structure
HEARTBEAT_TECHLOAD → vérifie système
```

### Option 2 : Sessions isolées

Des sessions Moltbot séparées avec des prompts dédiés :
- Session `collecteur` avec son propre SOUL
- Session `archiviste` avec son propre SOUL
- Etc.

### Option 3 : Sub-agents spawn

L'agent principal spawn des sub-agents pour des tâches spécifiques :
```
sessions_spawn(task="Vérifie les sources", label="collecteur")
```

**Recommandation :** Commencer par Option 1 (simple), migrer vers Option 2/3 si besoin d'isolation.

---

## Rapports

Chaque agent produit un rapport quand il détecte quelque chose :

```markdown
## Rapport Archiviste — 2025-01-31

### Alertes
- ⚠️ PENDING/ contient 12 fichiers > 7 jours
- ⚠️ Projet "Sidekicks" inactif depuis 45 jours

### Stats
- 7 projets actifs dans NOW/
- 324 fiches People (18 sans photo)
- 2540 fichiers dans PENDING/ (en cours de tri)

### Actions proposées
- [ ] Archiver Sidekicks ?
- [ ] Traiter les 12 fichiers PENDING urgents
```

---

*Cette architecture évolue avec l'usage. Le Tech Lead met à jour ce fichier.*
