## Inbox

Un point d'entrée unique. Tout converge vers INBOX.

---

### Sources de capture

Les sources sont configurées dans `_SYSTEM/2-Automate/sources/` :
- **email.md** — Emails (Gmail, Outlook, etc.)
- **messaging.md** — Messageries (WhatsApp, Telegram, etc.)
- **calendar.md** — Calendriers
- **files.md** — Fichiers déposés

La configuration active est dans `_SYSTEM/local/sources.md`.

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
- Fichier reçu → proposer de le router
- Information importante → proposer de documenter
- Nouvelle info sur un projet → mettre à jour l'index
- Dans le doute → INBOX

---

### Routage

**Où va quoi :**

| Type | Destination |
|------|-------------|
| Fichier lié à un projet | `DATA/NOW/[Projet]/` |
| Document en attente d'action | `DATA/PENDING/` |
| Archive/référence | `DATA/ARCHIVE/` |
| Idée/réflexion | `DATA/GARDEN/` |
| Pas clair | `DATA/INBOX/` (reste là) |

**Tu ne perds rien.** Si tu ne sais pas où mettre quelque chose → INBOX.
