#!/bin/bash
SERVICE=$1
if [ -z "$SERVICE" ]; then
  echo '{"status":"error","message":"service_name é obrigatório"}'
  exit 1
fi
STATUS=$(systemctl is-active "$SERVICE" 2>/dev/null || echo "inactive")
echo "{\"status\":\"success\",\"service\":\"$SERVICE\",\"active\":\"$STATUS\"}"
