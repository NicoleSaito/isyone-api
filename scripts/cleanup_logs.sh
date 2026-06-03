#!/bin/bash
DAYS=${1:-30}
find /var/log -name "*.log" -mtime +$DAYS -delete 2>/dev/null
COUNT=$(find /var/log -name "*.log" 2>/dev/null | wc -l)
echo "{\"status\":\"success\",\"message\":\"Logs com mais de $DAYS dias removidos\",\"logs_restantes\":$COUNT}"
