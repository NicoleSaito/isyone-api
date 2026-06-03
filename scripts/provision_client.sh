#!/bin/bash
CLIENT_ID=$1
CLIENT_NAME=$2
if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_NAME" ]; then
  echo '{"status":"error","message":"client_id e client_name são obrigatórios"}'
  exit 1
fi
mkdir -p "/opt/isyone/clients/$CLIENT_ID" 2>/dev/null
echo "{\"status\":\"success\",\"message\":\"Cliente '$CLIENT_NAME' provisionado\",\"client_id\":\"$CLIENT_ID\"}"
