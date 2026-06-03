from fastapi import APIRouter, Header, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from core.database import get_db, ScriptModel
from core.security import verify_token
from core.executor import run_script

router = APIRouter(prefix="/api/v1/scripts", tags=["Execução de Scripts"])


class RunScriptRequest(BaseModel):
    script_name: str
    parameters: Optional[list[str]] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "script_name": "provision_client",
                "parameters": ["cli_001", "Restaurante Bom Sabor"],
            }
        }
    }


@router.get(
    "/",
    summary="Listar scripts disponíveis",
    description="Retorna todos os scripts cadastrados e ativos.",
)
def list_scripts(
    x_isy_token: str = Header(...),
    db: Session = Depends(get_db),
):
    verify_token(db, x_isy_token)
    scripts = db.query(ScriptModel).filter(ScriptModel.active == True).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "filename": s.filename,
            "description": s.description,
            "parameters": s.parameters,
            "active": s.active,
        }
        for s in scripts
    ]


@router.post(
    "/run",
    summary="Executar um script",
    description="Executa um script cadastrado pelo nome, com os parâmetros informados. Requer header X-Isy-Token.",
)
def run(
    body: RunScriptRequest,
    x_isy_token: str = Header(...),
    db: Session = Depends(get_db),
):
    verify_token(db, x_isy_token)

    script = db.query(ScriptModel).filter(
        ScriptModel.name == body.script_name,
        ScriptModel.active == True,
    ).first()

    if not script:
        return {"status": "error", "message": f"Script '{body.script_name}' não encontrado ou inativo."}

    return run_script(script.filename, body.parameters or [], db)
