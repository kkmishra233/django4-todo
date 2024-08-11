#!/bin/bash
# uptime-check.sh

UPTIME_LIMIT=7200 # 2 hours in seconds

while true; do
    sleep $UPTIME_LIMIT # Check every minute
    UPTIME=$(awk '{print $1}' /proc/uptime)
    
    # Perform floating-point comparison using bc
    UPTIME_EXCEEDED=$(echo "$UPTIME > $UPTIME_LIMIT" | bc -l)
    
    if [ "$UPTIME_EXCEEDED" -eq 1 ]; then
        echo "Uptime limit exceeded. Stopping all processes." | tee /proc/1/fd/1
        echo "Current uptime: $UPTIME seconds" | tee /proc/1/fd/1
        echo "Uptime limit: $UPTIME_LIMIT seconds" | tee /proc/1/fd/1
        kill -TERM 1 # Send TERM signal to the supervisord process (pid 1)
        exit 1
    fi
done
