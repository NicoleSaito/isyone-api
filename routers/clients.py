from fastapi import APIRouter
from pydantic import BaseModel
from core.executor import run_script

router = APIRouter(prefix="/clients", tags=["Clientes"])


class ProvisionRequest(BaseModel):
    client_id: str
    client_name: str

    model_config = {
        "json_schema_extra": {
            "example": {"client_id": "cli_001", "client_name": "Restaurante Bom Sabor"}
        }
    }


class DeprovisionRequest(BaseModel):
    client_id: str

    model_config = {"json_schema_extra": {"example": {"client_id": "cli_001"}}}


@router.post(
    "/provision",
    summary="Provisionar novo cliente",
    description="Executa o script de provisionamento, criando diretório e configurações para um novo cliente.",
)
def provision_client(body: ProvisionRequest):
    return run_script("provision_client.sh", [body.client_id, body.client_name])


@router.delete(
    "/deprovision",
    summary="Desprovisionar cliente",
    description="Remove todos os recursos provisionados para o cliente informado.",
)
def deprovision_client(body: DeprovisionRequest):
    return run_script("deprovision_client.sh", [body.client_id])
