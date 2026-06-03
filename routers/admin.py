from fastapi import APIRouter, Header, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from core.database import get_db, ScriptModel, TokenModel
from core.security import verify_token

router = APIRouter(prefix="/api/v1/admin", tags=["Administração"])


class ScriptCreate(BaseModel):
    name: str
    filename: str
    description: Optional[str] = None
    parameters: Optional[str] = None
    active: bool = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "restart_nginx",
                "filename": "restart_nginx.sh",
                "description": "Reinicia o serviço nginx",
                "parameters": "none",
                "active": True,
            }
        }
    }


class ScriptUpdate(BaseModel):
    description: Optional[str] = None
    parameters: Optional[str] = None
    active: Optional[bool] = None


class TokenUpdate(BaseModel):
    new_token: str

    model_config = {"json_schema_extra": {"example": {"new_token": "meu-novo-token-secreto-2024"}}}


# ── Scripts ──────────────────────────────────────────────

@router.get("/scripts", summary="Listar todos os scripts (inclusive inativos)")
def list_all_scripts(x_isy_token: str = Header(...), db: Session = Depends(get_db)):
    verify_token(db, x_isy_token)
    scripts = db.query(ScriptModel).all()
    return scripts


@router.post("/scripts", summary="Cadastrar novo script")
def create_script(body: ScriptCreate, x_isy_token: str = Header(...), db: Session = Depends(get_db)):
    verify_token(db, x_isy_token)

    if db.query(ScriptModel).filter(ScriptModel.name == body.name).first():
        raise HTTPException(status_code=400, detail=f"Script '{body.name}' já existe.")

    script = ScriptModel(**body.model_dump())
    db.add(script)
    db.commit()
    db.refresh(script)
    return {"status": "success", "message": f"Script '{body.name}' cadastrado.", "id": script.id}


@router.patch("/scripts/{script_id}", summary="Atualizar script (ativar/desativar ou editar)")
def update_script(
    script_id: int,
    body: ScriptUpdate,
    x_isy_token: str = Header(...),
    db: Session = Depends(get_db),
):
    verify_token(db, x_isy_token)
    script = db.query(ScriptModel).filter(ScriptModel.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script não encontrado.")

    if body.description is not None:
        script.description = body.description
    if body.parameters is not None:
        script.parameters = body.parameters
    if body.active is not None:
        script.active = body.active

    db.commit()
    return {"status": "success", "message": f"Script '{script.name}' atualizado."}


@router.delete("/scripts/{script_id}", summary="Remover script")
def delete_script(script_id: int, x_isy_token: str = Header(...), db: Session = Depends(get_db)):
    verify_token(db, x_isy_token)
    script = db.query(ScriptModel).filter(ScriptModel.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script não encontrado.")
    db.delete(script)
    db.commit()
    return {"status": "success", "message": f"Script removido."}


# ── Token ──────────────────────────────────────────────

@router.put("/token", summary="Alterar token de autenticação dinamicamente")
def update_token(body: TokenUpdate, x_isy_token: str = Header(...), db: Session = Depends(get_db)):
    verify_token(db, x_isy_token)

    if len(body.new_token) < 12:
        raise HTTPException(status_code=400, detail="Token deve ter no mínimo 12 caracteres.")

    record = db.query(TokenModel).first()
    record.token = body.new_token
    record.updated_at = datetime.utcnow()
    db.commit()
    return {"status": "success", "message": "Token atualizado com sucesso."}
