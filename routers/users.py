from fastapi import APIRouter
from pydantic import BaseModel, Field
from core.executor import run_script

router = APIRouter(prefix="/users", tags=["Usuários Linux"])


class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=32, pattern=r"^[a-z0-9_]+$")
    password: str = Field(..., min_length=8)

    model_config = {
        "json_schema_extra": {
            "example": {"username": "cliente_joao", "password": "SenhaSegura123!"}
        }
    }


@router.post(
    "/",
    summary="Criar usuário Linux",
    description="Cria um novo usuário no sistema operacional via script bash.",
)
def create_user(body: CreateUserRequest):
    return run_script("create_user.sh", [body.username, body.password])
