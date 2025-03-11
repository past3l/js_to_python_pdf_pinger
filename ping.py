#!/bin/bash

# pdf_monitor.sh
LOG_FILE="/root/pdf_pings/pdf_clicks.log"
PORT=8765

# Renk kodları
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Log dizini oluştur
mkdir -p /root/pdf_pings

# Başlık
clear
echo -e "${GREEN}=== PDF Ping Monitörü ===${NC}"
echo -e "${BLUE}Port: ${PORT}${NC}"
echo -e "${BLUE}Log: ${LOG_FILE}${NC}"
echo -e "${RED}Ctrl+C ile çıkış${NC}\n"

# Tcpdump ile izle ve logla
tcpdump -n -i any port $PORT -l -A | while read line; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${GREEN}[${TIMESTAMP}]${NC} ${line}" | tee -a $LOG_FILE
done
