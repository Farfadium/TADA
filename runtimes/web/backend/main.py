"""TADA Web API — FastAPI backend pour capture et consultation."""
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

import config
from services import (
    get_dashboard_stats,
    quick_capture,
    quick_capture_file,
    process_file_analysis,
    get_pending_items,
    get_now_projects,
    get_file_tree,
    get_file_content,
    chat_with_moltbot,
)

# App
app = FastAPI(title="TADA Web API", version="0.2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


# Models
class LoginRequest(BaseModel):
    username: str
    password: str


class CaptureRequest(BaseModel):
    content: str
    force_pending: bool = False


class ChatRequest(BaseModel):
    message: str
    runtime: str = "claude"  # moltbot, claude, moltbot-web


class Token(BaseModel):
    access_token: str
    token_type: str


# Auth helpers
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


# Routes
@app.get("/api")
async def api_root():
    return {"name": "TADA Web API", "version": "0.2.0", "status": "running"}


@app.post("/auth/login", response_model=Token)
async def login(req: LoginRequest):
    """Login et génération JWT."""
    if req.username != config.ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if config.ADMIN_PASSWORD_HASH:
        if not pwd_context.verify(req.password, config.ADMIN_PASSWORD_HASH):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": req.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/dashboard")
async def dashboard(current_user: str = Depends(get_current_user)):
    """Récupère les stats du dashboard."""
    return get_dashboard_stats()


@app.get("/projects")
async def projects(current_user: str = Depends(get_current_user)):
    """Liste les projets actifs (NOW/)."""
    return get_now_projects()


@app.get("/pending")
async def pending(current_user: str = Depends(get_current_user)):
    """Liste les items en PENDING/."""
    return get_pending_items()


@app.get("/files/tree")
async def files_tree(path: str = "", current_user: str = Depends(get_current_user)):
    """Récupère l'arborescence des fichiers."""
    return get_file_tree(path)


@app.get("/files/content")
async def files_content(path: str, current_user: str = Depends(get_current_user)):
    """Lit le contenu d'un fichier."""
    result = get_file_content(path)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.post("/capture")
async def capture(req: CaptureRequest, current_user: str = Depends(get_current_user)):
    """Capture rapide d'une information."""
    return quick_capture(req.content, force_pending=req.force_pending)


@app.post("/capture/file")
async def capture_file_route(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    description: str = Form(""),
    current_user: str = Depends(get_current_user)
):
    """Capture d'un fichier (audio, image, etc.)."""
    result = await quick_capture_file(file, description)

    if result.get("analysis_pending") and "_bg_params" in result:
        bg_params = result.pop("_bg_params")
        background_tasks.add_task(process_file_analysis, **bg_params)

    return result


@app.get("/runtimes")
async def list_runtimes(current_user: str = Depends(get_current_user)):
    """Liste les runtimes disponibles."""
    from runtimes_config import get_available_runtimes
    return {"runtimes": get_available_runtimes()}


@app.post("/chat")
async def chat(req: ChatRequest, current_user: str = Depends(get_current_user)):
    """Chat avec le runtime sélectionné."""
    from runtimes_config import get_runtime
    runtime = get_runtime(req.runtime)
    
    if runtime["type"] == "gateway":
        # Utiliser Moltbot Gateway
        from moltbot_client import chat_with_gateway
        response = await chat_with_gateway(
            req.message,
            gateway_url=runtime["gateway_url"],
            token=runtime["gateway_token"],
            session_key=runtime["session_key"]
        )
    else:
        # Utiliser Claude API direct
        response = await chat_with_moltbot(req.message, current_user)
    
    return {"response": response, "runtime": req.runtime}


@app.get("/chat/history")
async def get_history(limit: int = 50, current_user: str = Depends(get_current_user)):
    """Récupère l'historique de la conversation avec Moltbot."""
    try:
        from moltbot_client import get_chat_history
        messages = await get_chat_history(limit)
        return {"messages": messages}
    except Exception as e:
        return {"messages": [], "error": str(e)}


@app.delete("/chat/history")
async def clear_chat_history(current_user: str = Depends(get_current_user)):
    """Efface l'historique de chat."""
    from services import chat_histories
    if current_user in chat_histories:
        chat_histories[current_user] = []
    return {"success": True}


# Serve frontend static files
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "dist"

if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve SPA - return index.html for all non-API routes."""
        file_path = FRONTEND_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
