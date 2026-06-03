FROM python:3.11-slim

WORKDIR /app

# Instala bash para executar os scripts
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências primeiro (cache de layers)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Diretório onde os scripts serão montados via volume
RUN mkdir -p /opt/isyone/scripts

# Variáveis de ambiente padrão
ENV SCRIPTS_DIR=/opt/isyone/scripts
ENV DATABASE_URL=sqlite:///./isyone.db

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
