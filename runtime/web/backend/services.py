"""Services pour lire/écrire dans TADA."""
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Any
import mimetypes
import base64

import config

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = bool(config.ANTHROPIC_API_KEY)
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = bool(config.OPENAI_API_KEY)
except ImportError:
    OPENAI_AVAILABLE = False


def get_dashboard_stats() -> Dict[str, Any]:
    """Récupère les stats pour le dashboard."""
    stats = {
        "now_projects": 0,
        "pending_items": 0,
        "pending_old": 0,  # > 7 jours
        "last_sync": None,
    }

    # Compter les projets NOW
    if config.NOW_DIR.exists():
        stats["now_projects"] = len([
            d for d in config.NOW_DIR.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ])

    # Compter PENDING (récursivement dans tous les sous-répertoires)
    if config.PENDING_DIR.exists():
        pending_files = [
            f for f in config.PENDING_DIR.rglob("*")
            if f.is_file() and not f.name.startswith(".")
        ]
        stats["pending_items"] = len(pending_files)

        # Vérifier les vieux fichiers (> 7 jours)
        now = datetime.now()
        for f in pending_files:
            age_days = (now.timestamp() - f.stat().st_mtime) / 86400
            if age_days > 7:
                stats["pending_old"] += 1

    # Dernière sync (via git)
    git_dir = config.TADA_ROOT / ".git"
    if git_dir.exists():
        head_file = git_dir / "FETCH_HEAD"
        if head_file.exists():
            stats["last_sync"] = datetime.fromtimestamp(head_file.stat().st_mtime).isoformat()

    return stats


def get_now_projects() -> List[Dict[str, Any]]:
    """Liste les projets actifs."""
    projects = []

    if not config.NOW_DIR.exists():
        return projects

    for project_dir in config.NOW_DIR.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith("."):
            continue

        index_file = project_dir / "index.md"
        project_info = {
            "name": project_dir.name,
            "path": str(project_dir.relative_to(config.DATA_DIR)),
            "has_index": index_file.exists(),
        }

        # Lire le statut depuis l'index si disponible
        if index_file.exists():
            content = index_file.read_text()
            # Chercher un statut (🟢, 🟡, 🔴, etc.)
            status_match = re.search(r'[🟢🟡🔴⚪]', content)
            if status_match:
                project_info["status"] = status_match.group()

        projects.append(project_info)

    return projects


def get_pending_items() -> List[Dict[str, Any]]:
    """Liste les items en PENDING (récursivement dans tous les sous-répertoires)."""
    items = []

    if not config.PENDING_DIR.exists():
        return items

    for item_file in config.PENDING_DIR.rglob("*"):
        if not item_file.is_file() or item_file.name.startswith("."):
            continue

        age_days = (datetime.now().timestamp() - item_file.stat().st_mtime) / 86400

        items.append({
            "name": item_file.name,
            "path": str(item_file.relative_to(config.DATA_DIR)),
            "age_days": round(age_days, 1),
            "is_old": age_days > 7,
        })

    return sorted(items, key=lambda x: x["age_days"], reverse=True)


def quick_capture(content: str, force_pending: bool = False) -> Dict[str, Any]:
    """Capture rapide d'une information.

    Analyse le contenu pour:
    - Détecter les tags (#tag)
    - Détecter les projets (@projet)
    - Détecter les liens ([[lien]])
    - Router vers le bon endroit
    """
    # Détection
    tags = re.findall(r'#(\w+)', content)
    projects = re.findall(r'@([\w-]+)', content)
    links = re.findall(r'\[\[([^\]]+)\]\]', content)

    # Routage
    destination = "PENDING"
    target_file = None

    if not force_pending and len(projects) == 1:
        # Un seul projet mentionné → essayer de router
        project_name = projects[0]
        project_dir = config.NOW_DIR / project_name

        if project_dir.exists():
            # Projet existe, ajouter au fichier _inbox.md du projet
            destination = f"NOW/{project_name}"
            target_file = project_dir / "_inbox.md"
        else:
            # Projet n'existe pas → PENDING
            destination = "PENDING"

    # Par défaut : PENDING
    if target_file is None:
        config.PENDING_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_file = config.PENDING_DIR / f"{timestamp}_capture.md"

    # Écriture
    header = f"""---
A quoi sert ce fichier:
Capture rapide du {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

"""

    # Ajouter métadonnées si détections
    metadata = []
    if tags:
        metadata.append(f"Tags: {', '.join(['#' + t for t in tags])}")
    if projects:
        metadata.append(f"Projets: {', '.join(['@' + p for p in projects])}")
    if links:
        metadata.append(f"Liens: {', '.join(['[[' + l + ']]' for l in links])}")

    if metadata:
        header += "\n".join(metadata) + "\n\n---\n\n"

    full_content = header + content + "\n"

    # Créer ou append
    if target_file.exists():
        # Append avec séparateur
        existing = target_file.read_text()
        target_file.write_text(existing + "\n\n---\n\n" + full_content)
    else:
        target_file.write_text(full_content)

    return {
        "success": True,
        "destination": destination,
        "file": str(target_file.relative_to(config.DATA_DIR)),
        "detected": {
            "tags": tags,
            "projects": projects,
            "links": links,
        },
    }


def analyze_image(image_path: Path) -> str:
    """Analyse une image avec GPT-4 Vision et retourne une description."""
    if not OPENAI_AVAILABLE:
        return "_[Analyse visuelle non disponible - clé API OpenAI manquante]_"

    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)

        # Lire l'image et l'encoder en base64
        image_data = image_path.read_bytes()
        image_base64 = base64.standard_b64encode(image_data).decode("utf-8")

        # Déterminer le type MIME
        mime_type = mimetypes.guess_type(str(image_path))[0] or "image/jpeg"

        # Appeler GPT-4 Vision
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Décris cette image de manière concise et utile. Identifie les éléments clés, le contexte, et tout ce qui pourrait être pertinent pour retrouver cette information plus tard. Réponds en français."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"_[Erreur lors de l'analyse: {str(e)}]_"


def transcribe_audio(audio_path: Path) -> str:
    """Transcrit un fichier audio avec Whisper et retourne le texte."""
    if not OPENAI_AVAILABLE:
        return "_[Transcription non disponible - clé API OpenAI manquante]_"

    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)

        # Whisper accepte directement les fichiers
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="fr"  # Français par défaut
            )

        return transcript.text
    except Exception as e:
        return f"_[Erreur lors de la transcription: {str(e)}]_"


def process_file_analysis(file_path: Path, md_path: Path, file_type: str, description: str, content_type: str, content_size: int):
    """Traite l'analyse AI en arrière-plan et met à jour le fichier .md."""
    try:
        # Analyser le contenu du fichier (principe TADA: tout doit être lisible)
        analysis = ""
        if file_type == "image":
            analysis = analyze_image(file_path)
        elif file_type == "audio":
            analysis = transcribe_audio(file_path)

        # Lire le contenu actuel du .md
        current_content = md_path.read_text()

        # Ajouter l'analyse avant le fichier original
        if analysis:
            if file_type == "image":
                analysis_section = f"## 👁️ Analyse visuelle\n\n{analysis}\n\n"
            elif file_type == "audio":
                analysis_section = f"## 🎤 Transcription\n\n{analysis}\n\n"
            else:
                analysis_section = ""

            # Remplacer le placeholder par l'analyse
            updated_content = current_content.replace(
                "_[Analyse en cours...]_\n\n",
                analysis_section
            )
            md_path.write_text(updated_content)
    except Exception as e:
        # En cas d'erreur, mettre à jour le .md avec l'erreur
        try:
            current_content = md_path.read_text()
            error_section = f"_[Erreur lors de l'analyse: {str(e)}]_\n\n"
            updated_content = current_content.replace(
                "_[Analyse en cours...]_\n\n",
                error_section
            )
            md_path.write_text(updated_content)
        except:
            pass  # Silently fail if we can't even write the error


async def quick_capture_file(file, description: str = "") -> Dict[str, Any]:
    """Capture d'un fichier (audio, image, etc.).

    Sauvegarde le fichier dans PENDING/ et crée un fichier .md associé.
    L'analyse AI se fait en arrière-plan.
    """
    config.PENDING_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = Path(file.filename).suffix if file.filename else ""

    # Déterminer le type de fichier
    content_type = file.content_type or ""
    file_type = "fichier"
    if content_type.startswith("audio/"):
        file_type = "audio"
    elif content_type.startswith("image/"):
        file_type = "image"
    elif content_type.startswith("video/"):
        file_type = "video"

    # Sauvegarder le fichier
    file_path = config.PENDING_DIR / f"{timestamp}_{file_type}{file_extension}"
    content = await file.read()
    file_path.write_bytes(content)

    # Créer le fichier .md associé immédiatement (sans attendre l'analyse)
    md_path = config.PENDING_DIR / f"{timestamp}_{file_type}.md"

    md_content = f"""---
A quoi sert ce fichier:
Capture {file_type} du {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

# Capture {file_type}

**Fichier :** `{file_path.name}`
**Type :** {content_type}
**Taille :** {len(content)} octets

"""

    if description:
        md_content += f"**Description :** {description}\n\n"

    # Ajouter un placeholder pour l'analyse en cours
    if file_type in ["image", "audio"]:
        md_content += "_[Analyse en cours...]_\n\n"

    md_content += f"## Fichier original\n\n![[{file_path.name}]]\n"

    md_path.write_text(md_content)

    return {
        "success": True,
        "destination": "PENDING",
        "file": str(file_path.relative_to(config.DATA_DIR)),
        "md_file": str(md_path.relative_to(config.DATA_DIR)),
        "type": file_type,
        "analysis_pending": file_type in ["image", "audio"],
        # Les paramètres pour le background task
        "_bg_params": {
            "file_path": file_path,
            "md_path": md_path,
            "file_type": file_type,
            "description": description,
            "content_type": content_type,
            "content_size": len(content),
        }
    }
