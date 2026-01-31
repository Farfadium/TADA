## Inbox

Point d'entrée unique. L'IA trie automatiquement — ce qui reste dans INBOX attend une décision humaine.

---

### Sources de capture

Les sources sont configurées dans `_SYSTEM/2-Automate/sources/` :
- **email.md** — Emails (Gmail, Outlook, etc.)
- **messaging.md** — Messageries (WhatsApp, Telegram, etc.)
- **calendar.md** — Calendriers
- **files.md** — Fichiers déposés

La configuration active est dans `_SYSTEM/local/TOOLS.md`.

---

### Comportement de l'IA

**À chaque session :**
- Exécuter la routine `sync` pour récupérer les nouvelles informations
- Proposer le tri si INBOX non vide

**À chaque message :**
- Détecter les tags (`#emails`, `#revue`, `#projet`, etc.)
- Identifier les fichiers mentionnés ou joints
- Extraire les informations à stocker

**Ce que tu fais :**
- Tag détecté → exécuter la routine correspondante
- Fichier reçu → router directement si clair, sinon demander
- Information importante → documenter directement
- Nouvelle info sur un projet → mettre à jour l'index
- Pas clair → INBOX + poser la question immédiatement

---

### Routage

**Où va quoi :**

| Type | Destination |
|------|-------------|
| Fichier lié à un projet | `DATA/NOW/[Projet]/` |
| Archive/référence | `DATA/ARCHIVE/` |
| Idée/réflexion | `DATA/ARCHIVE/Garden/` |
| Pas clair | `DATA/INBOX/` + demander |

**INBOX = décision humaine requise.** L'IA ne laisse pas traîner — elle demande où classer.
