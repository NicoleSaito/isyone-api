import re
from fastapi import Header, HTTPException
from sqlalchemy.orm import Session
from core.database import TokenModel


BLOCKED_PATTERNS = [
    r"[;&|`$]",          # separadores de comando
    r"\.\./",            # path traversal
    r">(>?)",            # redirecionamento
    r"<",                # redirecionamento
    r"\$\(",             # command substitution
    r"\bsudo\b",
    r"\brm\s+-rf\b",
    r"\bchmod\b",
    r"\bchown\b",
    r"\bnc\b",
    r"\bcurl\b",
    r"\bwget\b",
]


def verify_token(db: Session, x_isy_token: str):
    record = db.query(TokenModel).first()
    if not record or x_isy_token != record.token:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou ausente. Use o header X-Isy-Token.",
        )
    return x_isy_token


def sanitize_param(value: str) -> str:
    """
    Valida um parâmetro contra command injection.
    Lança HTTPException 400 se detectar padrão malicioso.
    """
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, value, re.IGNORECASE):
            raise HTTPException(
                status_code=400,
                detail=f"Parâmetro inválido: padrão bloqueado detectado '{pattern}'.",
            )
    # Permite apenas alfanuméricos, ponto, hífen, underline e arroba
    if not re.match(r"^[a-zA-Z0-9._\-@ ]+$", value):
        raise HTTPException(
            status_code=400,
            detail="Parâmetro contém caracteres não permitidos.",
        )
    return value.strip()
