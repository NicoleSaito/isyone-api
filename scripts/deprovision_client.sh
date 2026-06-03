#!/bin/bash
CLIENT_ID=$1
if [ -z "$CLIENT_ID" ]; then
  echo '{"status":"error","message":"client_id é obrigatório"}'
  exit 1
fi
rm -rf "/opt/isyone/clients/$CLIENT_ID" 2>/dev/null
echo "{\"status\":\"success\",\"message\":\"Cliente '$CLIENT_ID' removido\"}"
