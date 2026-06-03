#!/bin/bash
# Libera uma porta no firewall via ufw
# Uso: ./open_port.sh <port> <protocol>

PORT=$1
PROTO=${2:-tcp}

if [ -z "$PORT" ]; then
  echo '{"status":"error","message":"Porta é obrigatória"}'
  exit 1
fi

if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
  echo '{"status":"error","message":"Porta inválida (use 1-65535)"}'
  exit 1
fi

ufw allow "$PORT/$PROTO" 2>/dev/null
echo "{\"status\":\"success\",\"message\":\"Porta $PORT/$PROTO liberada no firewall\"}"
