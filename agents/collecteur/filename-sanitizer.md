---
A quoi sert ce fichier:
Fonction de normalisation des noms de fichiers pour éviter les caractères incompatibles avec les systèmes de fichiers
---

# Filename Sanitizer

**Règle absolue : Tous les noms de fichiers créés par le collecteur DOIVENT passer par cette fonction de nettoyage.**

## Fonction de normalisation

```python
import re
import unicodedata

def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Normalise un nom de fichier pour être compatible avec tous les systèmes de fichiers.

    Règles appliquées:
    - Normalise Unicode (NFC)
    - Supprime emojis et symboles
    - Supprime caractères de contrôle
    - Remplace caractères spéciaux par underscores
    - Limite la longueur
    - Garde uniquement: a-z A-Z 0-9 - _ . ( ) [ ]

    Args:
        filename: Nom de fichier à nettoyer
        max_length: Longueur max (défaut: 200)

    Returns:
        Nom de fichier nettoyé et sécurisé
    """
    # Normaliser Unicode (décomposer puis recomposer)
    normalized = unicodedata.normalize('NFC', filename)

    # Séparer nom et extension
    parts = normalized.rsplit('.', 1)
    name = parts[0]
    ext = parts[1] if len(parts) > 1 else ''

    # Supprimer emojis (plage Unicode principale)
    name = re.sub(r'[\U0001F300-\U0001F9FF]', '_', name)

    # Supprimer autres symboles problématiques
    name = re.sub(r'[🎥🎨💌💬📕🥂⏳🎄🧑‍🕵🏻‍♂]', '_', name)

    # Supprimer caractères de contrôle et replacement char
    name = re.sub(r'[\u0000-\u001f\u007f-\u009f\ufffd]', '_', name)

    # Remplacer caractères spéciaux par underscores
    # Garde uniquement: lettres, chiffres, tirets, underscores, points, parenthèses, crochets
    name = re.sub(r'[^\w\s\-.()\[\]]+', '_', name, flags=re.UNICODE)

    # Remplacer espaces multiples par un seul underscore
    name = re.sub(r'\s+', '_', name)

    # Supprimer underscores multiples
    name = re.sub(r'_+', '_', name)

    # Supprimer underscores au début/fin
    name = name.strip('_')

    # Limiter la longueur (en gardant de la place pour l'extension)
    if ext:
        max_name_length = max_length - len(ext) - 1  # -1 pour le point
        name = name[:max_name_length]
    else:
        name = name[:max_length]

    # Reconstruire le nom complet
    if ext:
        return f"{name}.{ext}"
    return name

# Exemples d'utilisation
# sanitize_filename("2024-07-01_🎥_Case_Study.md")
# -> "2024-07-01___Case_Study.md"
#
# sanitize_filename("Email_avec_'apostrophe'_et_«guillemets».md")
# -> "Email_avec_apostrophe_et_guillemets.md"
#
# sanitize_filename("Домен_EVANEOS.RU_срок_регистрации.md")
# -> "______EVANEOS_RU____________.md"
```

## Utilisation

### Dans les scripts de collection

```python
from filename_sanitizer import sanitize_filename

# Lors de la création d'un fichier email
subject = email['subject']
filename = f"{date}_{sender}_{subject}.md"
filename = sanitize_filename(filename)  # TOUJOURS nettoyer avant de créer

# Lors de la création d'un fichier calendar
title = event['title']
filename = f"{date}_{title}_{event_id}.md"
filename = sanitize_filename(filename)  # TOUJOURS nettoyer
```

### Dans MCP Tools

Si les MCP tools créent des fichiers directement, ils doivent aussi utiliser cette fonction.

## Vérification

Pour vérifier que tous les fichiers sont conformes:

```bash
# Chercher les fichiers avec des caractères problématiques
find DATA/PENDING -name "*[🎥🎨💌💬📕🥂⏳]*" -o -name "*�*"
```

## Migration des fichiers existants

Pour nettoyer les fichiers existants, voir les instructions Moltbot dans ce fichier.
