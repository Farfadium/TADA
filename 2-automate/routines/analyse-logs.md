### Analyse des logs

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Temps | Mensuel (1er du mois) |
| Tag | #analyse-logs |

**Contexte :**
Analyser l'historique des conversations pour identifier les patterns, problèmes récurrents, et améliorations possibles du système TADA.

**Emplacement des logs :** `_SYSTEM/local/Claude_logs/`

**Actions :**

1. **Lister les conversations**
   ```bash
   ls -lhS "_SYSTEM/local/Claude_logs/"*.jsonl
   ```

2. **Extraire les messages utilisateur de toutes les conversations**
   ```bash
   for f in "_SYSTEM/local/Claude_logs/"*.jsonl; do
     cat "$f" | jq -r 'select(.type == "user") | .message.content[] | select(.type == "text") | .text'
   done
   ```

3. **Identifier les patterns** :
   - Questions répétées (= documentation manquante)
   - Micro-validations fréquentes ("oui", "go") (= manque d'autonomie)
   - Demandes de mise à jour d'index (= routine à automatiser)
   - Problèmes non résolus qui reviennent
   - Hésitations sur la structure/nommage

4. **Catégoriser les findings** :

   | Catégorie | Symptôme | Solution type |
   |-----------|----------|---------------|
   | Documentation | Question répétée | Ajouter dans CLAUDE.md |
   | Autonomie | Micro-validations | Ajouter aux "actions sans validation" |
   | Routine | Action récurrente manuelle | Créer/améliorer routine |
   | Bug | Problème qui revient | Logger dans issues.md |
   | Structure | Hésitation sur organisation | Clarifier dans formats.md |

5. **Produire un rapport** dans `_SYSTEM/local/analyse-logs.md` :
   ```markdown
   # Analyse des logs — [YYYY-MM-DD]

   ## Conversations analysées
   - X conversations
   - Période : [date début] → [date fin]

   ## Patterns identifiés

   ### Documentation manquante
   - ...

   ### Manque d'autonomie
   - ...

   ### Routines à créer/améliorer
   - ...

   ### Problèmes récurrents
   - ...

   ## Actions proposées
   | Priorité | Action | Fichier concerné |
   |----------|--------|------------------|
   | 1 | ... | ... |
   ```

6. **Proposer les améliorations** au système

**Validation requise :** Oui (pour les modifications du système)

**Exemple :**
```
#analyse-logs

Je lis les 19 conversations dans _SYSTEM/local/Claude_logs/...

---

## Patterns identifiés

### Documentation manquante
- "Quand commence une session?" (3 fois)
- "Comment marche ton contexte?" (2 fois)
→ Ajouter section "Fonctionnement Claude" dans CLAUDE.md

### Manque d'autonomie
- 47 micro-validations ("oui", "go", "ok")
→ Définir les actions que je peux faire seul

### Problèmes récurrents
- "GARDEN qui revient" (2 fois, non résolu)
→ Créer _SYSTEM/local/issues.md

---

## Actions proposées
| Priorité | Action |
|----------|--------|
| 1 | Créer section "Comment Claude fonctionne" |
| 2 | Définir liste d'actions autonomes |
| 3 | Créer issues.md |

Valider ?
```
