from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import clients, users, infra

app = FastAPI(
    title="Isy.one Automation API",
    description="""
## API de Automação — Isy.one

Expõe scripts bash de provisionamento e gerenciamento de clientes via endpoints REST.

### Funcionalidades
- **Clientes**: provisionar e desprovisionar ambientes de clientes
- **Usuários Linux**: criar usuários no sistema operacional
- **Infraestrutura**: gerenciar serviços e regras de firewall

### Como funciona
Cada endpoint recebe parâmetros JSON, valida os dados e executa o script bash correspondente no servidor Linux, retornando o resultado em formato JSON.
    """,
    version="1.0.0",
    contact={"name": "Isy.one", "url": "https://isyone.com.br"},
    license_info={"name": "MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clients.router)
app.include_router(users.router)
app.include_router(infra.router)


@app.get("/", tags=["Status"], summary="Health check")
def root():
    return {
        "status": "online",
        "app": "Isy.one Automation API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Status"], summary="Verificar saúde da API")
def health():
    return {"status": "healthy"}
