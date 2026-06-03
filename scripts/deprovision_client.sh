#!/bin/bash
# Remove provisionamento de um cliente
# Uso: ./deprovision_client.sh <client_id>

CLIENT_ID=$1

if [ -z "$CLIENT_ID" ]; then
  echo '{"status":"error","message":"client_id é obrigatório"}'
  exit 1
fi

BASE_DIR="/opt/isyone/clients"
CLIENT_DIR="$BASE_DIR/$CLIENT_ID"

if [ ! -d "$CLIENT_DIR" ]; then
  echo "{\"status\":\"error\",\"message\":\"Cliente '$CLIENT_ID' não encontrado\"}"
  exit 1
fi

rm -rf "$CLIENT_DIR" 2>/dev/null
echo "{\"status\":\"success\",\"message\":\"Cliente '$CLIENT_ID' desprovisionado com sucesso\"}"
