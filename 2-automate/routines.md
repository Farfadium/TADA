## Routines & Maintenance

Le système s'auto-maintient. Les routines exécutent, l'IA apprend et documente.

---

### Routines

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
| Init système | | DATA/NOW/ vide | #setup |
| Init projet | | | #init |
| Tri INBOX | | Fichier en INBOX | |
| Tri emails | | | #emails |
| Revue projets | Vendredi | | #revue |
| Mise à jour index | | Fichier ajouté/supprimé | #maj-index |
| Mise à jour projet | | | #projet |
| Ajout règle | | | #rule |
| Analyse logs | 1er du mois | | #analyse-logs |
| Commit | | Modifications significatives | #commit, #sync |

**Détails des routines :** `_SYSTEM/2-Automate/routines/[nom].md`

---

### Auto-amélioration

**Quand tu apprends quelque chose, tu le documentes :**

| Information apprise | Fichier à mettre à jour |
|--------------------|------------------------|
| Règle sur une source (email, etc.) | `2-Automate/sources/[source].md` (notes) |
| Configuration spécifique | `local/TOOLS.md` |
| Préférence utilisateur | Fichier concerné dans `_SYSTEM/` |
| Résultat de routine | `local/logs.md` |
| Décision utilisateur | `local/logs.md` (section Décisions) |

**Exemple :**
> Utilisateur : "Les emails de newsletters, archive-les directement"

→ Tu ajoutes dans `2-Automate/sources/email.md` (section Notes) :
```
- Newsletters → archiver directement (sans validation)
```

---

### Logging

**Emplacement :** `_SYSTEM/local/logs.md`

| Type | Quand | Format |
|------|-------|--------|
| **Routines** | À chaque exécution | Date, routine, résultat, notes |
| **Décisions** | Quand l'utilisateur répond à une proposition | Date, proposition, réponse, action |
| **Actions** | Actions significatives | Date, description |

**Routines :**
- Savoir quand relancer une routine périodique
- Identifier les routines non utilisées (→ proposer suppression)

**Décisions utilisateur :**
- "Connecter WhatsApp ?" → non → Ne plus proposer pendant 30j
- "Archiver ce projet ?" → plus tard → Reproposer dans 7j

**Actions :**
- Création/modification de fichiers importants
- Évolutions du système
- Sync effectuées

---

### Nettoyage automatique

**Routines non utilisées :**
- Si une routine n'a pas été exécutée depuis 60 jours → proposer suppression
- Logger la proposition et la réponse

**Sources non utilisées :**
- Si une source est configurée mais jamais syncée → alerter
- Proposer de la désactiver ou de la configurer correctement

**Index obsolètes :**
- Fichiers listés mais supprimés → nettoyer l'index
- Fichiers présents mais non listés → ajouter à l'index

---

### Règles de mise à jour

**Sans validation :**
- `local/logs.md`
- `local/TOOLS.md` (date de sync)
- Index (`*/index.md`) : ajout/suppression de fichiers listés

**Avec validation :**
- Instructions dans `_SYSTEM/*.md`
- Fichiers utilisateur hors `_SYSTEM/`
- Suppression de fichiers
- Création de nouvelles règles
