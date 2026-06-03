from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Literal
from core.executor import run_script

router = APIRouter(prefix="/infra", tags=["Infraestrutura"])


class OpenPortRequest(BaseModel):
    port: int = Field(..., ge=1, le=65535)
    protocol: Literal["tcp", "udp"] = "tcp"

    model_config = {"json_schema_extra": {"example": {"port": 8080, "protocol": "tcp"}}}


@router.post(
    "/firewall/open",
    summary="Liberar porta no firewall",
    description="Executa script para liberar uma porta via ufw.",
)
def open_port(body: OpenPortRequest):
    return run_script("open_port.sh", [body.port, body.protocol])


@router.get(
    "/services/{service_name}",
    summary="Verificar status de serviço",
    description="Consulta o status de um serviço systemd no servidor.",
)
def check_service(service_name: str):
    return run_script("check_service.sh", [service_name])
