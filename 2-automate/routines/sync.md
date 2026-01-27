### Sync

> Synchronisation + maintenance proactive du système TADA.

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Temps | Début de session |
| Tag | #sync |

---

## Actions

### 1. Sources — Récupérer les nouveautés

Lire `local/sources.md` pour identifier les sources actives.
Pour chaque source active, exécuter les actions définies dans `sources/[source].md` § "Actions sync".

### 2. Système — Maintenance automatique

| Vérification | Action |
|--------------|--------|
| Index obsolètes | Nettoyer les entrées orphelines |
| Fichiers non listés | Ajouter aux index |
| Date de sync | Mettre à jour `local/sources.md` |

### 3. Système — Diagnostic

- [ ] NOW/ a des projets actifs ?
- [ ] INBOX/ vide ?
- [ ] PENDING/ docs expirés ?
- [ ] Routines non exécutées > 30j ?
- [ ] Incohérences détectées ?

### 4. Output

```
**Sync** | [sources actives] | [X nouveautés]
🔧 [maintenance effectuée]
→ [action suggérée]
```

---

## Validation

**Sans validation :** récupération, maintenance index, mise à jour dates
**Avec validation :** actions proposées, évolutions système
