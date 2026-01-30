### TADA Next

> Session d'amélioration collaborative de TADA

**Déclencheurs :**
- `#tada-next`, `#next`, `#améliorer`
- "On fait quoi ?", "J'ai du temps"

**Impact :** Système + Contenu

---

## Actions

### 1. Audit rapide (30 sec)

**Pending / Rappels** (cron jobs) :
- Rappels en attente ou disabled
- Tâches TODO dans `memory/YYYY-MM-DD.md`

**Planning** (calendrier) :
- Events des 7 prochains jours liés aux projets actifs
- Prochains RDV importants à préparer

**Projets** (`DATA/NOW/`) :
- Nombre de fichiers (emails/meetings/docs)
- Index complet ?
- Fiches People manquantes ?

**Sources + Système** :
- Sources configurées vs manquantes
- Problèmes/idées ouverts

### 2. Propositions NUMÉROTÉES (format liste)

```
## TADA Next — [date]

### ⏰ Pending
1. [rappel] — [action: exécuter/replanifier/supprimer]

### 📅 Planning (7 jours)
2. [event] — [date] — [préparer quoi ?]

### 📁 Projets
3. **Projet A** (X fichiers) — [ce qui manque]
4. **Projet B** (vide) — à définir

### ⚡ Quick wins
5. [action] — [bénéfice]

### 🔧 Améliorations
6. [action] — [bénéfice]

---
Numéro ?
```

### 3. Exécuter le choix

- L'utilisateur répond avec un numéro
- Exécuter
- Documenter dans `memory/YYYY-MM-DD.md`

---

**Règle clé :** Tout numéroter. Pas de tables (mauvais rendu Telegram).
