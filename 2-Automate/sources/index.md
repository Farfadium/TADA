# Sources

> Configuration des sources de capture pour TADA.

---

## Catalogue complet

👉 **[[CATALOG.md]]** — Liste de toutes les sources possibles, classées par priorité.

Utilisé lors du bootstrap pour identifier et activer les sources de l'utilisateur.

---

## Sources implémentées

| Fichier | Source | Type | Statut |
|---------|--------|------|--------|
| [[email.md]] | Email | Gmail, Outlook, IMAP | 🟢 |
| [[calendar.md]] | Calendar | Google Calendar, Outlook | 🟢 |
| [[meetings.md]] | Meetings | Fireflies, Otter | 🟢 |
| [[folk.md]] | CRM | Folk API | 🟢 |
| [[miro.md]] | Boards | Miro API | 🟢 |
| [[files.md]] | Fichiers | Système local | 🟢 |
| [[messaging.md]] | Messagerie | WhatsApp, Telegram, Slack | 🔲 |

---

## Créer une nouvelle source

1. Copier `_template.md`
2. Remplir les sections :
   - **Configuration** : Comment accéder (API, MCP, export)
   - **Bootstrap** : Comment amorcer la source (collecte initiale)
   - **Comportement** : Ce que l'IA peut/ne peut pas faire
   - **Sync** : Fréquence et critères
   - **Format** : Structure des fichiers créés
3. Ajouter au catalogue `CATALOG.md`
4. Documenter le statut dans `TOOLS.md`

---

## Structure d'une source

Chaque fichier source doit contenir :

```markdown
## Configuration
- MCP / API / Export disponibles
- Accès : lecture / écriture / suppression

## Bootstrap
- Comment amorcer (collecte initiale)
- Période à récupérer
- Commandes / scripts

## Comportement
- Ce que l'IA peut faire
- Ce que l'IA ne fait JAMAIS

## Sync
- Fréquence (session, quotidien, temps réel)
- Critères de récupération

## Format
- Structure des fichiers créés
- Nommage
- Liens entre fichiers
```

---

## Configuration instance

La configuration spécifique (comptes actifs, MCP, dernière sync) est dans :

👉 `_SYSTEM/runtimes/[runtime]/TOOLS.md`
