## Logs

L'IA maintient un journal structuré de ses actions.

**Emplacement :** `_SYSTEM/local/logs.md`

**Ce qui est loggé :**

| Type | Quand | Format |
|------|-------|--------|
| **Routines** | À chaque exécution | Date, routine, résultat, notes |
| **Décisions** | Quand l'utilisateur répond à une proposition | Date, proposition, réponse, action |
| **Actions** | Actions significatives | Date, description |

---

### Routines

Chaque exécution de routine est tracée :
- **Date** : quand
- **Routine** : laquelle
- **Résultat** : `ok` | `partiel` | `échec`
- **Notes** : détails si nécessaire

**Utilité :**
- Savoir quand relancer une routine périodique
- Identifier les routines non utilisées (→ proposer suppression)
- Debugger les échecs

---

### Décisions utilisateur

Quand l'IA propose quelque chose et que l'utilisateur répond :
- **Date** : quand
- **Proposition** : ce qui a été proposé
- **Réponse** : `oui` | `non` | `plus tard`
- **Action** : ce que l'IA doit faire suite à cette réponse

**Exemples :**
- "Connecter WhatsApp ?" → non → Ne plus proposer pendant 30j
- "Créer un label Gmail pour ce projet ?" → oui → Créé
- "Archiver ce projet ?" → plus tard → Reproposer dans 7j

---

### Actions

Journal chronologique des actions significatives effectuées par l'IA.

**Ce qui est loggé :**
- Création/modification de fichiers importants
- Évolutions du système
- Sync effectuées
- Anomalies détectées
