## Routines

Les routines sont des actions prédéfinies que tu exécutes selon des déclencheurs précis.

**Types de déclencheurs :**

| Type | Description | Exemples |
|------|-------------|----------|
| **Temps** | Périodicité ou date | `session`, `7j`, `Vendredi`, `1er du mois` |
| **Logique** | Condition détectée | `Fichier déposé`, `Document en attente` |
| **Tag** | Mot-clé dans le message utilisateur | `#emails`, `#revue`, `#projet` |

**Comment exécuter une routine :**

1. **Identifier le déclencheur** — L'utilisateur dit `#emails` ? → routine Tri emails
2. **Lire la routine** — Suivre les actions dans l'ordre
3. **Valider si requis** — Certaines actions nécessitent confirmation
4. **Logger** — Tracer l'exécution dans `local/logs.md`

**Utilisation proactive des routines :**

Quand l'utilisateur te demande quelque chose qui ressemble à une routine existante, **utilise la routine sans demander**. Exemples :
- "commit" → routine Commit
- "trie mes emails" → routine Tri emails
- "on en est où sur les projets ?" → routine Revue projets

Tu n'as pas besoin du tag exact. Si l'intention correspond, exécute la routine.

**Tableau des routines :**

| Routine | Temps | Logique | Tag |
|---------|-------|---------|-----|
| **Sync** | session | | #sync |
| Init système | | NOW/ vide | #setup |
| Init projet | | | #init |
| Tri INBOX | 7j sans tri | Fichier déposé | |
| Tri emails | | | #emails |
| Revue projets | Vendredi | | #revue |
| Alerte PENDING | | Document en attente | |
| Mise à jour index | | Fichier ajouté/supprimé | #maj-index |
| Mise à jour projet | | | #projet |
| Ajout règle | | | #rule |
| Analyse logs | 1er du mois | | #analyse-logs |
| Commit | | Modifications significatives | #commit, #sync |

**Détails des routines :** `_SYSTEM/2-Automate/routines/[nom].md`

Quand tu exécutes une routine, lis d'abord le fichier correspondant pour connaître les actions à effectuer.
