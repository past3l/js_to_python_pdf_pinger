#!/bin/bash

# Log dosyası
LOG_FILE="/root/pdf_pings/clicks.log"

# Log dizini oluştur
mkdir -p /root/pdf_pings

# Başlık
echo "=== PDF İzleme Başladı ==="
echo "Port: 8765"
echo "Log: $LOG_FILE"
echo "Ctrl+C ile çıkış"
echo "------------------------"

# Tcpdump ile izle
tcpdump -n -i any port 8765 -l | while read line; do
    if [[ $line == *"GET"* ]]; then
        timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        source_ip=$(echo $line | grep -oP 'IP \K[0-9.]+(?=\.)')
        echo "[$timestamp] Tıklama - IP: $source_ip" | tee -a "$LOG_FILE"
    fi
done
