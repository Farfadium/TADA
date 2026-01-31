# HEARTBEAT — Curateur

## Checks à chaque run

### 1. PENDING/ (priorité haute)
```bash
# Compter les fichiers
find DATA/PENDING -type f | wc -l

# Fichiers > 7 jours
find DATA/PENDING -type f -mtime +7
```

**Actions :**
- Trier les nouveaux fichiers (destination claire → déplacer)
- Lister les fichiers ambigus pour décision humaine
- Alerter si fichiers > 7 jours

### 2. NOW/ (priorité moyenne)
```bash
# Dernière modification par projet
for dir in DATA/NOW/*/; do
  echo "$dir: $(find "$dir" -type f -printf '%T@\n' | sort -n | tail -1)"
done
```

**Actions :**
- Projets inactifs > 30 jours → proposer archivage
- Projets sans index.md → alerter
- Sections vides dans index.md → alerter

### 3. TASKS-INDEX.md (priorité moyenne)
**Actions :**
- Scanner tous les TASKS.md dans DATA/
- Régénérer l'index consolidé
- Alerter sur tâches @due dans les 7 prochains jours

### 4. Cohérence liens (priorité basse)
**Actions :**
- Vérifier les liens internes cassés
- Détecter fichiers orphelins (jamais référencés)

## Limites par run

- Max 50 fichiers triés par run (éviter surcharge)
- Max 5 propositions en attente (ne pas accumuler)
- Si propositions non traitées > 3 jours → rappel

## État persistant

Fichier : `DATA/.curateur-state.json`

```json
{
  "lastRun": "2025-01-31T10:00:00Z",
  "pendingCount": 2450,
  "proposalsPending": 3,
  "lastFullScan": "2025-01-28T10:00:00Z"
}
```

## Output

Rapport dans `DATA/memory/curateur/YYYY-MM-DD.md`
Alertes urgentes → notification à Cassiopée
