#!/bin/bash
# Provisiona um novo cliente: cria diretório, permissões e arquivo de config
# Uso: ./provision_client.sh <client_id> <client_name>

CLIENT_ID=$1
CLIENT_NAME=$2

if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_NAME" ]; then
  echo '{"status":"error","message":"client_id e client_name são obrigatórios"}'
  exit 1
fi

BASE_DIR="/opt/isyone/clients"
CLIENT_DIR="$BASE_DIR/$CLIENT_ID"

mkdir -p "$CLIENT_DIR" 2>/dev/null
chmod 750 "$CLIENT_DIR" 2>/dev/null

cat > "$CLIENT_DIR/config.env" 2>/dev/null <<EOF
CLIENT_ID=$CLIENT_ID
CLIENT_NAME=$CLIENT_NAME
CREATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
STATUS=active
EOF

echo "{\"status\":\"success\",\"message\":\"Cliente '$CLIENT_NAME' provisionado\",\"path\":\"$CLIENT_DIR\"}"
