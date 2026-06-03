# Isy.one Automation API

API RESTful em Python (FastAPI) para execução de scripts bash de provisionamento de clientes do sistema **Isy.one**.

## Tecnologias

- **Python 3.11+**
- **FastAPI** — framework web moderno com validação automática e docs interativas
- **Uvicorn** — servidor ASGI de alta performance
- **Pydantic** — validação de dados via type hints

## Arquitetura

```
isyone-api/
├── main.py              # Entrypoint da aplicação
├── requirements.txt
├── core/
│   └── executor.py      # Motor de execução de scripts bash
├── routers/
│   ├── clients.py       # Endpoints de provisionamento de clientes
│   ├── users.py         # Endpoints de usuários Linux
│   └── infra.py         # Endpoints de serviços e firewall
└── scripts/
    ├── provision_client.sh
    ├── deprovision_client.sh
    ├── create_user.sh
    ├── check_service.sh
    └── open_port.sh
```

## Como rodar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar o servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Acessar a documentação interativa

Abra no navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

A documentação Swagger é gerada automaticamente pelo FastAPI.

## Endpoints disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Health check |
| `GET` | `/health` | Status da API |
| `POST` | `/clients/provision` | Provisionar novo cliente |
| `DELETE` | `/clients/deprovision` | Desprovisionar cliente |
| `POST` | `/users/` | Criar usuário Linux |
| `POST` | `/infra/firewall/open` | Liberar porta no firewall |
| `GET` | `/infra/services/{name}` | Verificar status de serviço |

## Como adicionar novos scripts

1. Coloque o script em `scripts/meu_script.sh`
2. Certifique-se de que o script retorna JSON no stdout:
   ```bash
   echo '{"status":"success","message":"ok"}'
   ```
3. Crie um endpoint no router adequado (ou crie um novo router):
   ```python
   @router.post("/minha-rota")
   def minha_rota(body: MeuRequest):
       return run_script("meu_script.sh", [body.parametro])
   ```
4. Se criou um novo router, registre-o no `main.py`.

## Pontos de evolução (MVP → Produção)

- Autenticação via API Key ou JWT
- Fila de execução para scripts de longa duração (Celery + Redis)
- Log persistente de todas as execuções
- Integração com SSH remoto via Paramiko para execução em outros servidores
- Contêinerização com Docker
- Pipeline CI/CD para deploy automático
