from fastapi import APIRouter, Header, Depends, Query
from sqlalchemy.orm import Session
from core.database import get_db, LogModel
from core.security import verify_token

router = APIRouter(prefix="/api/v1/logs", tags=["Logs e Auditoria"])


@router.get(
    "/",
    summary="Histórico de execuções",
    description="Retorna os logs de todas as execuções com filtro opcional por status.",
)
def get_logs(
    x_isy_token: str = Header(...),
    status: str = Query(None, description="Filtrar por 'success' ou 'error'"),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    verify_token(db, x_isy_token)

    query = db.query(LogModel).order_by(LogModel.executed_at.desc())
    if status:
        query = query.filter(LogModel.status == status)

    logs = query.limit(limit).all()
    return [
        {
            "id": l.id,
            "script_name": l.script_name,
            "parameters": l.parameters,
            "status": l.status,
            "output": l.output,
            "error": l.error,
            "executed_at": l.executed_at.isoformat(),
        }
        for l in logs
    ]


@router.get("/summary", summary="Resumo de execuções")
def get_summary(x_isy_token: str = Header(...), db: Session = Depends(get_db)):
    verify_token(db, x_isy_token)

    total = db.query(LogModel).count()
    success = db.query(LogModel).filter(LogModel.status == "success").count()
    error = db.query(LogModel).filter(LogModel.status == "error").count()

    return {
        "total_execucoes": total,
        "sucesso": success,
        "erro": error,
        "taxa_sucesso": f"{round((success / total * 100), 1)}%" if total else "0%",
    }
