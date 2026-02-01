# HEARTBEAT — Collecteur

## Checks à chaque run

### 1. État des sources (priorité haute)

```bash
# Lire tous les status.json
for f in _SYSTEM/2-Automate/sources/*-status.json; do
  echo "=== $f ==="
  cat "$f" | jq '{source, status, issues}'
done
```

**Actions :**
- Sources `partial` ou `error` → tenter de compléter
- Issues avec `action` → exécuter l'action
- Token/auth expirés → alerter immédiatement

### 2. Données manquantes (priorité haute)

**Gmail attachments :**
```bash
# Comparer emails avec attachments vs attachments téléchargés
# Si delta > 0 → télécharger les manquants
```

**Miro boards :**
```bash
# Vérifier si rate limit reset
# Si oui → télécharger les boards manquants
```

### 3. Nouvelles données (priorité moyenne)

Pour chaque source active :
- Vérifier s'il y a de nouvelles données depuis lastSync
- Si oui → lancer sync incrémentale
- Mettre à jour le status.json

### 4. Intégrité (priorité basse)

- Vérifier que les fichiers dans PENDING/ sont lisibles
- Détecter les fichiers corrompus ou vides
- Alerter si problème

## Fréquence

| Check | Fréquence |
|-------|-----------|
| État sources | Quotidien (matin) |
| Données manquantes | Quotidien |
| Nouvelles données | Quotidien ou sur demande |
| Intégrité | Hebdomadaire |

## Seuils d'alerte

| Situation | Action |
|-----------|--------|
| Source en erreur | 🔴 Alerte immédiate |
| Token expire < 7j | ⚠️ Alerte |
| Données manquantes > 10% | ⚠️ Alerte |
| Pas de sync > 7j | ⚠️ Alerte |

## État persistant

Fichiers `*-status.json` dans `_SYSTEM/2-Automate/sources/`

## Output

- Mise à jour des `*-status.json`
- Mise à jour de `STATUS.md`
- Rapport si anomalie détectée
