### Sync

> Synchronisation des sources de capture au démarrage.

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Temps | Début de session |
| Tag | #sync |

**Contexte :**
À chaque nouvelle session, l'IA récupère les nouvelles informations depuis toutes les sources configurées. L'objectif est d'avoir un système à jour dès le départ.

---

## Actions

### 1. Lire la configuration

- Lire `_SYSTEM/local/sources.md`
- Identifier les sources actives
- Noter la date de dernière sync pour chaque source

### 2. Pour chaque source active

**Email :**
- Récupérer les emails reçus depuis la dernière sync
- Critères : inbox, non traités
- Si nouveaux emails → proposer tri ou afficher résumé

**Calendar :**
- Récupérer les événements du jour + 7 jours
- Identifier les RDV liés aux projets actifs
- Alerter sur les échéances proches

**Files :**
- Lister INBOX/
- Identifier les fichiers non triés
- Si fichiers présents → proposer routage

**Messaging :**
- Si configuré : récupérer les messages non lus
- Extraire les informations importantes

### 3. Diagnostic système

Vérifier :
- [ ] NOW/ a des projets actifs ?
- [ ] INBOX/ est vide ou trié ?
- [ ] PENDING/ a des docs expirés ?
- [ ] Sources non configurées à proposer ?

### 4. Proposer des actions

Basé sur le diagnostic, proposer 1-3 actions prioritaires :
- "Tu as 5 emails non triés, on s'en occupe ?"
- "Le compromis dans PENDING expire dans 3 jours"
- "NOW/ est vide, on fait un tour de tes projets ?"

### 5. Mettre à jour les logs

- Logger la sync dans `local/logs.md`
- Mettre à jour `dernière sync` dans `local/sources.md`

---

## Validation requise

Non pour la récupération.
Oui pour les actions proposées.

---

## Output

```
**Sync terminée**

📧 Email : X nouveaux (depuis [date])
📅 Calendar : X événements cette semaine
📁 Files : X fichiers dans INBOX

**Actions suggérées :**
1. [action prioritaire]
2. [action secondaire]
```
