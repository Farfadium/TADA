### Alerte PENDING

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Logique | Document en attente depuis trop longtemps |
| Temps | Hebdomadaire (lors de la revue) |

**Contexte :**
Les documents dans PENDING/ attendent une action externe (signature, réponse, décision). Il faut surveiller qu'ils n'y restent pas indéfiniment.

**Actions :**

1. Lister les fichiers dans `PENDING/`
2. Vérifier la date de chaque fichier (préfixe `YYYY-MM-DD`)
3. Alerter si un document attend depuis plus de 7 jours
4. Proposer :
   - Une relance (brouillon email)
   - Une décision (archiver, abandonner, relancer)

**Validation requise :** Oui

**Format de présentation :**
```
## Documents en attente

| Fichier | Depuis | Action proposée |
|---------|--------|-----------------|
| 2026-01-15_Devis_Travaux.pdf | 12 jours | Relancer artisan |
| 2026-01-20_Contrat_Location.pdf | 7 jours | Attendre encore |

Quelle action pour chaque document ?
```
