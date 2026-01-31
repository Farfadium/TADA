---
description: Configuration source Apple Contacts — sync carnet d'adresses macOS/iCloud vers People/
---

# Apple Contacts

> Carnet d'adresses macOS/iOS — contacts, groupes, synchronisé via iCloud.

**Type :** `contacts`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [ ] API officielle (pas d'API REST)
- [x] MCP disponible (apple-mcp, pyapple-mcp)
- [x] Export manuel (vCard)
- [x] Scraping/autre (AppleScript, Contacts.framework)

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `apple-mcp` | Collection outils Apple natifs | [GitHub](https://github.com/supermemoryai/apple-mcp) |
| `pyapple-mcp` | Python, multi-apps Apple | [GitHub](https://github.com/54yyyu/pyapple-mcp) |
| `iMCP` | App macOS, Messages+Contacts+Reminders | [GitHub](https://github.com/mattt/iMCP) |

**MCP recommandé :** `apple-mcp` (complet, bien maintenu)

**Credentials nécessaires :**
- macOS uniquement
- Permissions Contacts pour l'app cliente
- iCloud activé (optionnel, pour sync multi-device)

**Permissions :**
- [x] Lecture (contacts, groupes)
- [x] Écriture (création, modification)
- [ ] Suppression (avec confirmation)

---

## Bootstrap (collecte initiale)

**Méthode 1 : Via MCP**
```bash
# Configurer dans Claude Desktop :
{
  "mcpServers": {
    "apple": {
      "command": "npx",
      "args": ["-y", "@anthropic/apple-mcp"]
    }
  }
}
```

**Méthode 2 : Export vCard**
1. Ouvrir Contacts.app
2. Sélectionner tous les contacts (⌘A)
3. File → Export → Export vCard...
4. Sauvegarder dans `DATA/PENDING/apple-contacts/`

**Méthode 3 : AppleScript**
```applescript
tell application "Contacts"
  repeat with p in people
    set n to name of p
    set e to value of first email of p
    log n & "," & e
  end repeat
end tell
```

**Période recommandée :** Tous les contacts

**Destination :** `DATA/PENDING/apple-contacts/`

---

## Format des fichiers

**Structure :**
```
apple-contacts/
├── index.md                    # Index alphabétique
├── groups/
│   ├── Famille.md
│   ├── Travail.md
│   └── ...
└── contacts/
    ├── A/
    │   ├── Alice-Dupont.md
    │   └── ...
    └── ...
```

**Format contact :**
```markdown
---
id: CONTACT_UUID
name: Prénom Nom
first_name: Prénom
last_name: Nom
nickname: Surnom
company: Entreprise
job_title: Titre
emails:
  - type: work
    value: pro@example.com
  - type: home
    value: perso@example.com
phones:
  - type: mobile
    value: +33 6 12 34 56 78
  - type: work
    value: +33 1 23 45 67 89
addresses:
  - type: home
    street: 123 Rue Example
    city: Paris
    postal_code: 75001
    country: France
birthday: 1990-05-15
groups: [Famille, Travail]
notes: Notes du contact
created: 2020-01-15
modified: 2024-06-20
---

# Prénom Nom

**Entreprise :** [[Orgs/Entreprise]]
**Poste :** Titre

## Contact

| Type | Valeur |
|------|--------|
| 📧 Email pro | pro@example.com |
| 📧 Email perso | perso@example.com |
| 📱 Mobile | +33 6 12 34 56 78 |
| ☎️ Travail | +33 1 23 45 67 89 |

## Adresse
123 Rue Example
75001 Paris, France

## Groupes
- [[Groups/Famille]]
- [[Groups/Travail]]

## Notes
[Notes du carnet d'adresses]

## Relations TADA
- Projets : [[NOW/Projet1]], [[NOW/Projet2]]
- Interactions : voir `_emails/`, `_meetings/`
```

---

## Sync incrémentale

**Fréquence :** quotidien ou session

**Via AppleScript :**
```applescript
tell application "Contacts"
  set recentContacts to people whose modification date > (current date) - 1 * days
end tell
```

**Critères :**
- Contacts modifiés depuis dernière sync
- Nouveaux contacts ajoutés
- Contacts supprimés

---

## Actions disponibles (via MCP)

**Lecture :**
- `search_contacts` — Recherche par nom, email, téléphone
- `get_contact` — Détails complet d'un contact
- `list_groups` — Lister les groupes
- `get_my_card` — Récupérer sa propre fiche

**Écriture :**
- `create_contact` — Créer un contact
- `update_contact` — Modifier un contact
- `add_to_group` — Ajouter à un groupe

---

## Mapping Apple Contacts → TADA

| Apple Contacts | TADA |
|----------------|------|
| Contact | `DATA/ARCHIVE/Répertoires/People/` |
| Groupe | Tag ou catégorie |
| Company | `DATA/ARCHIVE/Répertoires/Orgs/` |
| Notes | Section notes de la fiche |

---

## Enrichissement bidirectionnel

**Apple → TADA :**
- Coordonnées (email, tel, adresse)
- Groupes comme tags
- Notes basiques

**TADA → Apple :**
- Lien vers fiche TADA (dans notes)
- Mise à jour coordonnées si changement

**Règle de fusion :**
- Apple Contacts = source de vérité pour coordonnées
- TADA = source de vérité pour contexte, relations, historique

---

## Liens et relations

- Entreprise → [[Orgs/Entreprise]]
- Fiche TADA → [[People/Prénom Nom]]
- Groupes → Tags TADA

---

## Notes

**Limites :**
- macOS uniquement (pas d'API web iCloud)
- AppleScript requiert permissions
- vCard export peut être volumineux

**Sync iCloud :**
- Les contacts sont synchronisés via iCloud
- Modifications sur iOS/iPad apparaissent sur Mac
- Utiliser le Mac comme point de sync TADA

**Format vCard :**
```vcard
BEGIN:VCARD
VERSION:3.0
N:Nom;Prénom;;;
FN:Prénom Nom
ORG:Entreprise
TEL;type=CELL:+33612345678
EMAIL;type=WORK:email@example.com
END:VCARD
```

**Parser vCard :**
```bash
# Convertir vCard en JSON
npm install vcf
node -e "const vcf=require('vcf');console.log(vcf.parse(fs.readFileSync('contacts.vcf','utf8')))"
```

**Bonnes pratiques :**
- Garder Apple Contacts comme source principale
- Enrichir dans TADA avec contexte
- Sync régulière pour cohérence

_Les configurations spécifiques (groupes à surveiller) sont dans `local/TOOLS.md`._
