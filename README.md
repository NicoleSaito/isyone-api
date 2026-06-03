# IsyShell — Orquestrador Automático de Infraestrutura

![CI](https://github.com/NicoleSaito/isyone-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED)
![License](https://img.shields.io/badge/License-MIT-green)

API RESTful segura em Python para execução remota de scripts bash via HTTP, com autenticação por token, logs de auditoria persistidos em banco de dados e deploy containerizado com Docker.

> Projeto desenvolvido para o Hackathon Integrador — Isy.one

---

## Sumário

- [Contexto](#contexto)
- [Os 5 Pilares](#os-5-pilares)
- [Arquitetura](#arquitetura)
- [Como rodar](#como-rodar)
- [Endpoints](#endpoints)
- [Segurança](#segurança)
- [CI/CD](#cicd)
- [Próximos passos](#próximos-passos)

---

## Contexto

A Isy.one atende centenas de restaurantes parceiros que utilizam um agente de impressão local para o iFood. Sempre que é necessário atualizar o agente, limpar logs ou verificar containers Docker, a equipe de suporte precisa acessar o servidor manualmente via SSH para executar scripts de manutenção — o que gera gargalos operacionais.

O **IsyShell** elimina esse problema expondo esses scripts como endpoints REST seguros, auditáveis e executáveis remotamente sem acesso SSH.

---

## Os 5 Pilares

### 🛠️ API RESTful com Python
- Framework **FastAPI** com documentação Swagger automática
- Uso mandatório do `subprocess` para capturar `stdout` e `stderr` dos scripts
- Retorno JSON padronizado em todos os endpoints
- Endpoints para listagem, execução parametrizável e administração

### 🔐 Segurança
- Autenticação obrigatória via header `X-Isy-Token` em todas as rotas
- Sanitização contra **command injection**: bloqueia `;`, `&`, `|`, `$()`, `../`, `sudo`, `rm -rf` e outros padrões maliciosos
- Token configurável dinamicamente via endpoint administrativo

### ⚙️ Administração
- CRUD completo de scripts (cadastrar, editar, ativar/desativar, remover)
- Troca dinâmica do token de autenticação sem reiniciar a API
- Listagem de todos os scripts com status ativo/inativo

### 📋 Logs e Auditoria
- Persistência automática de cada execução no banco **SQLite**
- Dados registrados: horário exato, script invocado, parâmetros, status e output completo
- Endpoint de resumo com taxa de sucesso em tempo real

### 📦 Docker
- `Dockerfile` otimizado com imagem **python:3.11-slim**
- `docker-compose.yml` com volume mapeado para os scripts do host
- Banco de dados persistido fora do container via volume

---

## Arquitetura

```
isyone-api/
├── main.py                  # Entrypoint FastAPI
├── requirements.txt
├── Dockerfile               # Imagem python:3.11-slim
├── docker-compose.yml       # Volume para scripts e banco
├── core/
│   ├── database.py          # Models SQLAlchemy + init do banco
│   ├── executor.py          # Motor de execução + log automático
│   └── security.py          # Validação de token + sanitização
├── routers/
│   ├── scripts.py           # Listar e executar scripts
│   ├── admin.py             # CRUD de scripts e token
│   └── logs.py              # Histórico e resumo de execuções
└── scripts/
    ├── provision_client.sh
    ├── deprovision_client.sh
    ├── check_service.sh
    └── cleanup_logs.sh
```

---

## Como rodar

### Opção 1 — Docker (recomendado)

```bash
docker-compose up --build
```

A API sobe em `http://localhost:8000`.

### Opção 2 — Local

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Documentação interativa

Acesse `http://localhost:8000/docs` para o Swagger UI com todos os endpoints documentados e testáveis.

---

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Health check |
| `GET` | `/api/v1/scripts/` | Listar scripts ativos |
| `POST` | `/api/v1/scripts/run` | Executar um script |
| `GET` | `/api/v1/logs/` | Histórico de execuções |
| `GET` | `/api/v1/logs/summary` | Resumo e taxa de sucesso |
| `GET` | `/api/v1/admin/scripts` | Listar todos os scripts |
| `POST` | `/api/v1/admin/scripts` | Cadastrar novo script |
| `PATCH` | `/api/v1/admin/scripts/{id}` | Atualizar script |
| `DELETE` | `/api/v1/admin/scripts/{id}` | Remover script |
| `PUT` | `/api/v1/admin/token` | Alterar token dinamicamente |

Todas as rotas exigem o header `X-Isy-Token`.

**Token padrão para testes:**
```
544c5787-613a-4ac2-8e61-9e6486f8d74a
```

---

## Segurança

A API bloqueia automaticamente parâmetros que contenham padrões de command injection:

```bash
# Requisição bloqueada — retorna HTTP 400
POST /api/v1/scripts/run
{
  "script_name": "provision_client",
  "parameters": ["cliente; rm -rf /", "Hack"]
}

# Resposta
{
  "detail": "Parâmetro inválido: padrão bloqueado detectado '[;&|`$]'."
}
```

---

## CI/CD

O projeto possui pipeline de **Integração Contínua** via GitHub Actions que executa automaticamente a cada push na branch `main`:

1. Instala dependências
2. Inicializa o banco de dados
3. Executa todos os testes (autenticação, segurança, execução, logs)
4. Faz build da imagem Docker

---

## Próximos passos

- [ ] Fila de mensageria para execuções assíncronas (Celery + Redis)
- [ ] Notificações em tempo real via Telegram/WhatsApp ao fim de cada execução
- [ ] Interface web para gerenciamento visual dos scripts e logs
- [ ] Integração com SSH remoto via Paramiko para execução em servidores externos
- [ ] Autenticação com JWT e controle de permissões por usuário
- [ ] Migração do banco para PostgreSQL em produção