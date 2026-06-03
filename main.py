from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from routers import scripts, admin, logs

app = FastAPI(
    title="IsyShell — Isy.one Automation API",
    description="""
## IsyShell — Orquestrador Automático de Infraestrutura

API RESTful segura para execução de scripts bash via HTTP, com autenticação por token, logs de auditoria e administração dinâmica.

### Autenticação
Todas as rotas exigem o header **`X-Isy-Token`** com o token válido.

Token padrão para testes: `544c5787-613a-4ac2-8e61-9e6486f8d74a`

### Pilares implementados
- **API RESTful** com FastAPI e subprocess
- **Segurança** com X-Isy-Token e sanitização contra command injection
- **Administração** de scripts e token dinâmico
- **Logs e auditoria** persistidos em SQLite
- **Docker** com imagem leve python:3.11-slim
    """,
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scripts.router)
app.include_router(admin.router)
app.include_router(logs.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", tags=["Status"])
def root():
    return {
        "app": "IsyShell — Isy.one Automation API",
        "version": "2.0.0",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health", tags=["Status"])
def health():
    return {"status": "healthy"}
