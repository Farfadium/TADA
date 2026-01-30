"""Services pour lire/écrire dans TADA."""
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Any, Optional
import mimetypes
import base64
import os

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
        "pending_old": 0,
        "archive_items": 0,
        "memory_files": 0,
        "total_files": 0,
        "last_sync": None,
    }

    # Compter les projets NOW
    if config.NOW_DIR.exists():
        stats["now_projects"] = len([
            d for d in config.NOW_DIR.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ])

    # Compter PENDING
    if config.PENDING_DIR.exists():
        pending_files = list(config.PENDING_DIR.rglob("*"))
        pending_files = [f for f in pending_files if f.is_file() and not f.name.startswith(".")]
        stats["pending_items"] = len(pending_files)
        
        now = datetime.now()
        for f in pending_files:
            age_days = (now.timestamp() - f.stat().st_mtime) / 86400
            if age_days > 7:
                stats["pending_old"] += 1

    # Compter ARCHIVE
    if config.ARCHIVE_DIR.exists():
        stats["archive_items"] = len(list(config.ARCHIVE_DIR.rglob("*.md")))

    # Compter memory
    memory_dir = config.TADA_ROOT / "memory"
    if memory_dir.exists():
        stats["memory_files"] = len(list(memory_dir.glob("*.md")))

    # Total fichiers DATA
    if config.DATA_DIR.exists():
        stats["total_files"] = len(list(config.DATA_DIR.rglob("*")))

    # Dernière sync git
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
            "path": str(project_dir.relative_to(config.TADA_ROOT)),
            "has_index": index_file.exists(),
            "file_count": len(list(project_dir.rglob("*.md"))),
        }

        if index_file.exists():
            content = index_file.read_text()
            status_match = re.search(r'[🟢🟡🔴⚪]', content)
            if status_match:
                project_info["status"] = status_match.group()

        projects.append(project_info)

    return sorted(projects, key=lambda x: x["name"])


def get_pending_items() -> List[Dict[str, Any]]:
    """Liste les items en PENDING."""
    items = []

    if not config.PENDING_DIR.exists():
        return items

    def remove_surrogates(text: str) -> str:
        return ''.join(char if not (0xD800 <= ord(char) <= 0xDFFF) else '?' for char in text)

    for item_file in config.PENDING_DIR.rglob("*"):
        if not item_file.is_file() or item_file.name.startswith("."):
            continue

        try:
            age_days = (datetime.now().timestamp() - item_file.stat().st_mtime) / 86400
            safe_name = remove_surrogates(item_file.name)
            safe_path = remove_surrogates(str(item_file.relative_to(config.TADA_ROOT)))

            items.append({
                "name": safe_name,
                "path": safe_path,
                "age_days": round(age_days, 1),
                "is_old": age_days > 7,
                "size": item_file.stat().st_size,
            })
        except Exception:
            continue

    sorted_items = sorted(items, key=lambda x: x["age_days"], reverse=True)
    return sorted_items[:100]


def get_file_tree(root_path: str = "") -> Dict[str, Any]:
    """Récupère l'arborescence des fichiers TADA."""
    if root_path:
        base = config.TADA_ROOT / root_path
    else:
        base = config.TADA_ROOT

    if not base.exists():
        return {"error": "Path not found"}

    def build_tree(path: Path, depth: int = 0, max_depth: int = 3) -> Dict[str, Any]:
        if depth > max_depth:
            return {"name": path.name, "type": "dir", "truncated": True}

        result = {
            "name": path.name or str(path),
            "path": str(path.relative_to(config.TADA_ROOT)) if path != config.TADA_ROOT else "",
            "type": "dir" if path.is_dir() else "file",
        }

        if path.is_dir():
            children = []
            try:
                items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                for item in items[:50]:  # Limiter à 50 items par dossier
                    if item.name.startswith("."):
                        continue
                    if item.name == "node_modules":
                        continue
                    children.append(build_tree(item, depth + 1, max_depth))
            except PermissionError:
                pass
            result["children"] = children
            result["count"] = len(children)
        else:
            result["size"] = path.stat().st_size
            result["ext"] = path.suffix

        return result

    return build_tree(base)


def get_file_content(file_path: str) -> Dict[str, Any]:
    """Lit le contenu d'un fichier."""
    full_path = config.TADA_ROOT / file_path
    
    if not full_path.exists():
        return {"error": "File not found"}
    
    if not full_path.is_file():
        return {"error": "Not a file"}
    
    # Vérifier que le fichier est dans TADA_ROOT (sécurité)
    try:
        full_path.resolve().relative_to(config.TADA_ROOT.resolve())
    except ValueError:
        return {"error": "Access denied"}
    
    # Limiter la taille
    if full_path.stat().st_size > 1_000_000:  # 1MB
        return {"error": "File too large", "size": full_path.stat().st_size}
    
    try:
        content = full_path.read_text(encoding="utf-8")
        return {
            "path": file_path,
            "name": full_path.name,
            "content": content,
            "size": len(content),
        }
    except UnicodeDecodeError:
        return {"error": "Binary file", "path": file_path}


def quick_capture(content: str, force_pending: bool = False) -> Dict[str, Any]:
    """Capture rapide d'une information."""
    tags = re.findall(r'#(\w+)', content)
    projects = re.findall(r'@([\w-]+)', content)
    links = re.findall(r'\[\[([^\]]+)\]\]', content)

    destination = "PENDING"
    target_file = None

    if not force_pending and len(projects) == 1:
        project_name = projects[0]
        project_dir = config.NOW_DIR / project_name

        if project_dir.exists():
            destination = f"NOW/{project_name}"
            target_file = project_dir / "_inbox.md"

    if target_file is None:
        config.PENDING_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_file = config.PENDING_DIR / f"{timestamp}_capture.md"

    header = f"""---
A quoi sert ce fichier:
Capture rapide du {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

"""

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

    if target_file.exists():
        existing = target_file.read_text()
        target_file.write_text(existing + "\n\n---\n\n" + full_content)
    else:
        target_file.write_text(full_content)

    return {
        "success": True,
        "destination": destination,
        "file": str(target_file.relative_to(config.TADA_ROOT)),
        "detected": {"tags": tags, "projects": projects, "links": links},
    }


def analyze_image(image_path: Path) -> str:
    """Analyse une image avec GPT-4 Vision."""
    if not OPENAI_AVAILABLE:
        return "_[Analyse visuelle non disponible]_"

    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        image_data = image_path.read_bytes()
        image_base64 = base64.standard_b64encode(image_data).decode("utf-8")
        mime_type = mimetypes.guess_type(str(image_path))[0] or "image/jpeg"

        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Décris cette image de manière concise. Réponds en français."},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}}
                ]
            }]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"_[Erreur: {str(e)}]_"


def transcribe_audio(audio_path: Path) -> str:
    """Transcrit un fichier audio avec Whisper."""
    if not OPENAI_AVAILABLE:
        return "_[Transcription non disponible]_"

    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="fr"
            )
        return transcript.text
    except Exception as e:
        return f"_[Erreur: {str(e)}]_"


# Chat history per session (simple in-memory, resets on restart)
chat_histories: Dict[str, List[Dict[str, str]]] = {}

# Flag pour utiliser le vrai Moltbot
USE_REAL_MOLTBOT = True


async def chat_with_moltbot(message: str, username: str) -> str:
    """Chat avec Moltbot (le vrai, via Gateway WebSocket)."""
    
    if USE_REAL_MOLTBOT:
        try:
            from moltbot_client import chat_with_real_moltbot
            return await chat_with_real_moltbot(message)
        except Exception as e:
            # Fallback sur le mode local si le Gateway n'est pas disponible
            pass
    
    # Fallback: utiliser Claude/GPT directement
    stats = get_dashboard_stats()
    projects = get_now_projects()
    
    recent_memory = ""
    memory_dir = config.TADA_ROOT / "memory"
    if memory_dir.exists():
        memory_files = sorted(memory_dir.glob("*.md"), reverse=True)
        if memory_files:
            try:
                recent_memory = memory_files[0].read_text()[:1500]
            except:
                pass
    
    system_prompt = f"""Tu es l'assistant TADA de {username}. Tu as accès au système TADA.

## Contexte actuel
- {stats['now_projects']} projets actifs
- {stats['pending_items']} items en attente ({stats['pending_old']} > 7 jours)
- {stats['total_files']} fichiers total

## Projets actifs
{chr(10).join([f"- {p['name']} ({p['file_count']} fichiers)" for p in projects[:10]])}

## Mémoire récente
{recent_memory[:800] if recent_memory else "Pas de notes récentes"}

## Instructions
- Réponds en français, de manière concise
- Tu peux donner des conseils sur l'organisation
- Tu connais le système TADA (NOW/, PENDING/, ARCHIVE/)
- Sois utile et direct, pas de flatterie"""

    if ANTHROPIC_AVAILABLE:
        try:
            client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
            
            if username not in chat_histories:
                chat_histories[username] = []
            
            chat_histories[username].append({"role": "user", "content": message})
            history = chat_histories[username][-10:]
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=history
            )
            
            assistant_message = response.content[0].text
            chat_histories[username].append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
        except Exception as e:
            return f"Erreur Claude: {str(e)}"
    
    elif OPENAI_AVAILABLE:
        try:
            client = OpenAI(api_key=config.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erreur GPT: {str(e)}"
    
    return "Aucune API configurée"


def process_file_analysis(file_path: Path, md_path: Path, file_type: str, description: str, content_type: str, content_size: int):
    """Traite l'analyse AI en arrière-plan."""
    try:
        analysis = ""
        if file_type == "image":
            analysis = analyze_image(file_path)
        elif file_type == "audio":
            analysis = transcribe_audio(file_path)

        current_content = md_path.read_text()

        if analysis:
            if file_type == "image":
                analysis_section = f"## 👁️ Analyse visuelle\n\n{analysis}\n\n"
            elif file_type == "audio":
                analysis_section = f"## 🎤 Transcription\n\n{analysis}\n\n"
            else:
                analysis_section = ""

            updated_content = current_content.replace(
                "_[Analyse en cours...]_\n\n",
                analysis_section
            )
            md_path.write_text(updated_content)
    except Exception as e:
        try:
            current_content = md_path.read_text()
            error_section = f"_[Erreur: {str(e)}]_\n\n"
            updated_content = current_content.replace(
                "_[Analyse en cours...]_\n\n",
                error_section
            )
            md_path.write_text(updated_content)
        except:
            pass


async def quick_capture_file(file, description: str = "") -> Dict[str, Any]:
    """Capture d'un fichier (audio, image, etc.)."""
    config.PENDING_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = Path(file.filename).suffix if file.filename else ""

    content_type = file.content_type or ""
    file_type = "fichier"
    if content_type.startswith("audio/"):
        file_type = "audio"
    elif content_type.startswith("image/"):
        file_type = "image"
    elif content_type.startswith("video/"):
        file_type = "video"

    file_path = config.PENDING_DIR / f"{timestamp}_{file_type}{file_extension}"
    content = await file.read()
    file_path.write_bytes(content)

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

    if file_type in ["image", "audio"]:
        md_content += "_[Analyse en cours...]_\n\n"

    md_content += f"## Fichier original\n\n![[{file_path.name}]]\n"

    md_path.write_text(md_content)

    return {
        "success": True,
        "destination": "PENDING",
        "file": str(file_path.relative_to(config.TADA_ROOT)),
        "md_file": str(md_path.relative_to(config.TADA_ROOT)),
        "type": file_type,
        "analysis_pending": file_type in ["image", "audio"],
        "_bg_params": {
            "file_path": file_path,
            "md_path": md_path,
            "file_type": file_type,
            "description": description,
            "content_type": content_type,
            "content_size": len(content),
        }
    }
