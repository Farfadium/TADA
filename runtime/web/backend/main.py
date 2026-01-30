"""TADA Web API — FastAPI backend pour capture et consultation."""
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
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
)

# App
app = FastAPI(title="TADA Web API", version="0.1.0")

# CORS (à restreindre en prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restreindre à Tailscale
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


class Token(BaseModel):
    access_token: str
    token_type: str


# Auth helpers
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


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
@app.get("/")
async def root():
    return {"name": "TADA Web API", "version": "0.1.0", "status": "running"}


@app.post("/auth/login", response_model=Token)
async def login(req: LoginRequest):
    """Login et génération JWT."""
    # Simple auth pour MVP (un seul user)
    if req.username != config.ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Si pas de hash configuré, accepter n'importe quel mot de passe en dev
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


@app.post("/capture")
async def capture(req: CaptureRequest, current_user: str = Depends(get_current_user)):
    """Capture rapide d'une information."""
    result = quick_capture(req.content, force_pending=req.force_pending)
    return result


@app.post("/capture/file")
async def capture_file_route(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    description: str = Form(""),
    current_user: str = Depends(get_current_user)
):
    """Capture d'un fichier (audio, image, etc.)."""
    result = await quick_capture_file(file, description)

    # Si une analyse est nécessaire, la lancer en arrière-plan
    if result.get("analysis_pending") and "_bg_params" in result:
        bg_params = result.pop("_bg_params")
        background_tasks.add_task(
            process_file_analysis,
            **bg_params
        )

    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
