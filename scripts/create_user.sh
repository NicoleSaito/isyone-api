#!/bin/bash
# Cria um usuário Linux para um novo cliente
# Uso: ./create_user.sh <username> <password>

USERNAME=$1
PASSWORD=$2

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
  echo '{"status":"error","message":"Username e password são obrigatórios"}'
  exit 1
fi

if id "$USERNAME" &>/dev/null; then
  echo "{\"status\":\"error\",\"message\":\"Usuário '$USERNAME' já existe\"}"
  exit 1
fi

useradd -m -s /bin/bash "$USERNAME" 2>/dev/null
echo "$USERNAME:$PASSWORD" | chpasswd 2>/dev/null

echo "{\"status\":\"success\",\"message\":\"Usuário '$USERNAME' criado com sucesso\"}"
