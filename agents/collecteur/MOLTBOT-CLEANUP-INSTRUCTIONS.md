---
A quoi sert ce fichier:
Instructions pour Moltbot pour nettoyer les noms de fichiers sur le serveur GitHub
---

# Instructions de nettoyage pour Moltbot

## Contexte

Il y a ~2323 fichiers sur le repo GitHub avec des noms de fichiers problématiques :
- Emojis (🎥, 💬, 📕, etc.)
- Caractères Unicode invalides (�)
- Caractères cyrilliques mélangés avec du latin
- Ces fichiers ne peuvent pas être checkout sur macOS à cause de limitations du système de fichiers

## Mission pour Moltbot

**Renommer tous les fichiers problématiques sur GitHub pour qu'ils soient compatibles avec tous les systèmes de fichiers.**

## Instructions étape par étape

### 1. Cloner le repo sur un système Linux

```bash
cd /tmp
git clone https://github.com/Farfadium/TADA-YVAN.git
cd TADA-YVAN
```

> Sur Linux, le clone fonctionnera sans problème car Linux supporte ces caractères.

### 2. Télécharger le script de nettoyage

Créer `/tmp/cleanup-filenames.py` :

```python
#!/usr/bin/env python3
import os
import re
import unicodedata
import subprocess

def sanitize_filename(filename):
    """Nettoie un nom de fichier"""
    normalized = unicodedata.normalize('NFC', filename)

    # Séparer nom et extension
    parts = normalized.rsplit('.', 1)
    name = parts[0]
    ext = parts[1] if len(parts) > 1 else ''

    # Supprimer emojis
    name = re.sub(r'[\U0001F300-\U0001F9FF]', '_', name)
    name = re.sub(r'[🎥🎨💌💬📕🥂⏳🎄🧑‍🕵🏻‍♂]', '_', name)

    # Supprimer caractères de contrôle
    name = re.sub(r'[\u0000-\u001f\u007f-\u009f\ufffd]', '_', name)

    # Remplacer caractères spéciaux
    name = re.sub(r'[^\w\s\-.()\[\]]+', '_', name, flags=re.UNICODE)

    # Nettoyer espaces et underscores
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')

    # Limiter la longueur
    max_length = 200
    if ext:
        max_name_length = max_length - len(ext) - 1
        name = name[:max_name_length]
    else:
        name = name[:max_length]

    if ext:
        return f"{name}.{ext}"
    return name

# Parcourir tous les fichiers et renommer ceux qui ont besoin
rename_count = 0
for root, dirs, files in os.walk('.'):
    for filename in files:
        if filename.startswith('.git'):
            continue

        old_path = os.path.join(root, filename)
        clean_name = sanitize_filename(filename)

        if clean_name != filename:
            new_path = os.path.join(root, clean_name)

            # Vérifier que le nouveau nom n'existe pas déjà
            if os.path.exists(new_path):
                print(f"SKIP (conflit): {old_path}")
                continue

            print(f"RENAME:")
            print(f"  {old_path}")
            print(f"  -> {new_path}")

            os.rename(old_path, new_path)

            # Git add des deux côtés
            subprocess.run(['git', 'add', old_path], check=False)
            subprocess.run(['git', 'add', new_path], check=True)

            rename_count += 1

print(f"\n✅ {rename_count} fichiers renommés")
```

### 3. Exécuter le script de nettoyage

```bash
cd /tmp/TADA-YVAN
python3 /tmp/cleanup-filenames.py
```

### 4. Vérifier les changements

```bash
git status
git diff --stat --cached
```

### 5. Commiter et pusher

```bash
git commit -m "Clean: Normalize all filenames (remove emojis and invalid Unicode)

- Renamed ~2323 files with problematic characters
- Removed emojis, control characters, invalid Unicode
- Filesystem-safe names for better macOS compatibility

Co-Authored-By: Moltbot <moltbot@tada.ai>"

git push origin main
```

## Vérification post-nettoyage

Une fois pushé, vérifier sur macOS que le repo peut maintenant être cloné :

```bash
cd /tmp
git clone https://github.com/Farfadium/TADA-YVAN.git TADA-test
# Devrait fonctionner sans erreurs "Illegal byte sequence"
```

## Prévention future

Le collector a été mis à jour avec la fonction `sanitize_filename()` dans [[filename-sanitizer.md]].

Tous les nouveaux fichiers créés passeront automatiquement par cette fonction de nettoyage.
