#!/bin/bash
# Verifica se um serviço systemd está ativo
# Uso: ./check_service.sh <service_name>

SERVICE=$1

if [ -z "$SERVICE" ]; then
  echo '{"status":"error","message":"Nome do serviço é obrigatório"}'
  exit 1
fi

STATUS=$(systemctl is-active "$SERVICE" 2>/dev/null || echo "inactive")
ENABLED=$(systemctl is-enabled "$SERVICE" 2>/dev/null || echo "disabled")

echo "{\"status\":\"success\",\"service\":\"$SERVICE\",\"active\":\"$STATUS\",\"enabled\":\"$ENABLED\"}"
