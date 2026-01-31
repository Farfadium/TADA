---
description: Configuration source Signal — export conversations chiffrées vers TADA
---

# Signal

> Messagerie chiffrée — conversations privées, groupes, appels sécurisés.

**Type :** `messaging`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [ ] API officielle (pas d'API publique)
- [ ] MCP disponible (aucun officiel)
- [x] Export manuel (backup local chiffré)
- [x] Scraping/autre (signal-cli, SQLite)

**Outils disponibles :**
| Outil | Description | Lien |
|-------|-------------|------|
| `signal-cli` | CLI non-officiel | [GitHub](https://github.com/AsamK/signal-cli) |
| Signal Desktop | Backup local SQLite | Intégré |

**Prérequis :**
- Signal installé sur smartphone
- Signal Desktop lié (optionnel)
- Pour signal-cli : enregistrement ou linking

**Permissions :**
- [x] Lecture (via backup ou signal-cli)
- [x] Écriture (via signal-cli)
- [ ] Suppression (limité)

⚠️ **Sécurité :** Signal est conçu pour la confidentialité. L'extraction de données va à l'encontre du design sécuritaire.

---

## Bootstrap (collecte initiale)

**Méthode 1 : Backup iOS/Android (le plus sûr)**
```bash
# Android : Settings → Chats → Chat backups
# Le fichier backup est chiffré avec un code 30 chiffres

# Déchiffrer avec signal-backup-decode
pip install signal-backup-decode
signal-backup-decode backup.backup PASSPHRASE --output ./export/
```

**Méthode 2 : Signal Desktop SQLite**
```bash
# macOS
DB="$HOME/Library/Application Support/Signal/sql/db.sqlite"

# Linux
DB="$HOME/.config/Signal/sql/db.sqlite"

# La base est chiffrée avec SQLCipher
# Clé dans config.json : "key" field
```

**Méthode 3 : signal-cli**
```bash
# Installer
brew install signal-cli

# Lier à un compte existant (génère QR code)
signal-cli link -n "TADA sync"

# Récupérer les messages
signal-cli -u +33612345678 receive
```

**Période recommandée :** Conversations importantes seulement

**Destination :** `DATA/PENDING/signal/`

---

## Format des fichiers

**Structure :**
```
signal/
├── index.md
├── contacts/
│   ├── Jean-Dupont.md
│   └── ...
├── groups/
│   └── Groupe-1.md
└── media/
    └── ...
```

**Format conversation :**
```markdown
---
type: private
contact_uuid: UUID
contact_name: Jean Dupont
phone: +33612345678
message_count: 500
---

# Conversation avec [[Jean Dupont]]

**Téléphone :** +33 6 12 34 56 78
**Chiffré :** ✓ End-to-end

## Messages importants

### 2024-07-15
> Message important
> — Jean Dupont, 14:32

## Médias
- [[media/image-001.jpg]]
```

---

## Sync incrémentale

**Fréquence :** manuel (recommandé)

**Via signal-cli :**
```bash
# Recevoir nouveaux messages
signal-cli -u +33612345678 receive --json > messages.json

# Parser et intégrer dans TADA
```

---

## Détection nouvelles données

**Méthode disponible :**
- [ ] Webhook/Push (non disponible)
- [x] Polling API (signal-cli receive)
- [x] Sync manuelle uniquement

**signal-cli daemon mode :**
```bash
# Lancer en mode daemon avec DBus
signal-cli -u +33612345678 daemon

# Ou en mode JSON-RPC
signal-cli -u +33612345678 daemon --socket /tmp/signal.sock

# Les messages arrivent en temps réel sur le socket
```

**Polling avec signal-cli :**
```bash
# Récupérer les messages en attente
signal-cli -u +33612345678 receive --json

# Réponse
{
  "envelope": {
    "source": "+33698765432",
    "timestamp": 1720012345678,
    "dataMessage": {
      "message": "Hello",
      "timestamp": 1720012345678
    }
  }
}
```

**SQLite polling (Desktop) :**
```sql
-- Requête sur la base Signal Desktop
SELECT * FROM messages 
WHERE received_at > $LAST_SYNC
ORDER BY received_at;
```

**Setup requis :**
1. signal-cli installé et lié au compte
2. Ou accès à la base Signal Desktop
3. Clé SQLCipher pour déchiffrer la DB
4. Script de polling régulier

**Fréquence recommandée :**
- signal-cli daemon : quasi temps réel
- Polling : toutes les 5-15 minutes
- Manual : selon besoin

**⚠️ Limitations :**
- signal-cli consomme les messages (ils ne restent pas)
- La base Desktop est verrouillée quand l'app tourne
- Backup Android = extraction manuelle

---

## Actions disponibles (via signal-cli)

**Lecture :**
- `receive` — Recevoir messages en attente
- `listGroups` — Lister groupes
- `listContacts` — Lister contacts

**Écriture :**
- `send` — Envoyer message
- `sendTyping` — Indicateur de frappe
- `sendReceipt` — Accusé de réception

---

## Mapping Signal → TADA

| Signal | TADA |
|--------|------|
| Contact | [[People/Nom]] |
| Group | Groupe ou projet |
| Media | `_signal/media/` |

---

## Notes

**Chiffrement :**
- Signal = E2E encryption
- Les backups sont chiffrés
- SQLCipher pour la base locale

**signal-cli limitations :**
- Nécessite un numéro de téléphone dédié
- Ou linking (consomme un slot d'appareil)
- Pas de support des appels

**Alternatives :**
- Matrix bridge (Element)
- Pas de solution parfaite

**Bonnes pratiques :**
- Utiliser pour archive seulement
- Ne pas automatiser l'envoi
- Respecter la confidentialité

**Sécurité :**
- Ne jamais exposer les clés SQLCipher
- Chiffrer les exports
- Supprimer les données sensibles après traitement

_Les configurations spécifiques sont dans `local/TOOLS.md`._
