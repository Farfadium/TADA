---
description: Configuration source iCloud Drive — sync fichiers Apple cloud vers TADA
---

# iCloud Drive

> Stockage cloud Apple — fichiers, dossiers, intégration apps Apple.

**Type :** `files`

**Statut :** Voir `_SYSTEM/local/TOOLS.md` pour la configuration active.

---

## Configuration

**Type d'accès :**
- [ ] API officielle (pas d'API publique)
- [x] MCP disponible (via apple-mcp, limité)
- [x] Export manuel (dossier sync macOS)
- [x] Scraping/autre (CloudKit private DB)

**MCPs disponibles :**
| MCP | Description | Lien |
|-----|-------------|------|
| `apple-mcp` | Collection outils Apple | [GitHub](https://github.com/supermemoryai/apple-mcp) |

**MCP recommandé :** `apple-mcp` (accès limité aux fichiers)

**Prérequis :**
- macOS avec iCloud Drive activé
- Fichiers synchronisés localement

**Permissions :**
- [x] Lecture (via système de fichiers local)
- [x] Écriture (copie vers iCloud Drive)
- [ ] Suppression (via Finder)

⚠️ **Note :** Apple ne fournit pas d'API REST publique pour iCloud Drive.

---

## Bootstrap (collecte initiale)

**Méthode principale : Dossier sync local (macOS)**
```bash
# iCloud Drive synchronisé localement
ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs"

# Copier tout
cp -r "$ICLOUD"/* DATA/PENDING/icloud/

# Ou dossiers spécifiques
cp -r "$ICLOUD/Documents"/* DATA/PENDING/icloud/Documents/
```

**Forcer le téléchargement des fichiers cloud-only :**
```bash
# Liste fichiers cloud-only (icône nuage)
find "$ICLOUD" -name "*.icloud" -type f

# Forcer download (ouvrir le fichier)
open "$ICLOUD/chemin/vers/fichier.pdf"
```

**Période recommandée :** Tout ou dossiers spécifiques

**Destination :** `DATA/PENDING/icloud/`

---

## Format des fichiers

**Structure locale iCloud :**
```
~/Library/Mobile Documents/com~apple~CloudDocs/
├── Documents/
├── Downloads/
├── com~apple~Numbers/           # App-specific
├── com~apple~Pages/
└── ...
```

**Structure TADA :**
```
icloud/
├── index.md
├── Documents/
│   ├── file.pdf
│   └── file.pdf.md
└── ...
```

**Format métadonnées :**
```markdown
---
name: document.pdf
path: Documents/document.pdf
size: 1234567
created: 2024-01-15
modified: 2024-07-15
source: iCloud Drive
---

# document.pdf

**Chemin :** Documents/document.pdf
**Taille :** 1.2 MB
**Modifié :** 2024-07-15

## Contenu
[Résumé si extrait]
```

---

## Sync incrémentale

**Fréquence :** session (via filesystem watch)

**Détection des changements :**
```bash
# Fichiers modifiés dans les dernières 24h
find "$ICLOUD" -mtime -1 -type f
```

**Avec fswatch :**
```bash
fswatch -r "$ICLOUD" | while read file; do
  echo "Modifié: $file"
  # Sync vers TADA
done
```

---

## Fichiers cloud-only (.icloud)

**Problème :** Les fichiers non téléchargés sont des stubs `.icloud`

**Détection :**
```bash
# Lister fichiers cloud-only
find "$ICLOUD" -name ".*.icloud" -type f
```

**Format stub :**
```xml
<?xml version="1.0"?>
<!DOCTYPE plist ...>
<plist version="1.0">
<dict>
  <key>NSURLNameKey</key>
  <string>NomFichier.pdf</string>
</dict>
</plist>
```

**Forcer le téléchargement :**
```bash
# Option 1: brctl
brctl download "$ICLOUD/chemin/.fichier.icloud"

# Option 2: ouvrir
open "$ICLOUD/chemin/fichier.pdf"
```

---

## Apps spécifiques

**Dossiers par app :**
```
com~apple~Pages/     → Pages documents
com~apple~Numbers/   → Numbers spreadsheets
com~apple~Keynote/   → Keynote presentations
com~apple~Notes/     → Notes (pas accessible directement)
```

**Export apps :**
- Pages/Numbers/Keynote → Exporter en PDF/Office
- Notes → Utiliser MCP Apple Notes séparé

---

## Notes

**Limites :**
- Pas d'API publique (contrairement à Google/Dropbox)
- Accès uniquement via macOS/iOS
- Fichiers cloud-only = téléchargement manuel

**Alternatives pour accès API :**
- `pyicloud` : Librairie Python non-officielle (risqué)
- `icloud-drive-docker` : Container pour sync

**Sécurité :**
- iCloud chiffré end-to-end (Advanced Data Protection)
- Ne pas stocker tokens en clair

**Bonnes pratiques :**
- Utiliser la sync locale macOS
- Forcer le téléchargement des fichiers importants
- Automatiser via scripts shell

_Les configurations spécifiques sont dans `local/TOOLS.md`._
