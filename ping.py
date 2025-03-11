#!/bin/bash

# Yapılandırma
LOG_DIR="/root/pdf_pings"
LOG_FILE="$LOG_DIR/detailed_clicks.log"
HTML_LOG="$LOG_DIR/clicks.html"
PORT=8765

# Renkler
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Dizinleri oluştur
mkdir -p "$LOG_DIR"

# URL decode fonksiyonu
urldecode() {
    python3 -c "import sys, urllib.parse; print(urllib.parse.unquote(sys.stdin.read()))"
}

# HTML başlığı oluştur
cat > "$HTML_LOG" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>PDF İzleme Sistemi</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .click { border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .timestamp { color: #2196F3; }
        .ip { color: #4CAF50; }
        .details { margin-left: 20px; color: #666; }
    </style>
</head>
<body>
    <h1>PDF İzleme Sistemi</h1>
    <div id="clicks">
EOF

# Başlık
clear
echo -e "${GREEN}=== PDF İzleme Sistemi ===${NC}"
echo -e "${BLUE}Port: ${PORT}${NC}"
echo -e "${BLUE}Log Dosyası: ${LOG_FILE}${NC}"
echo -e "${BLUE}HTML Rapor: ${HTML_LOG}${NC}"
echo -e "${RED}Ctrl+C ile çıkış${NC}\n"

# Tcpdump ile izle ve parse et
tcpdump -n -i any port $PORT -l -A | while read line; do
    if [[ $line == *"GET"* ]]; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        SOURCE_IP=$(echo $line | grep -oP 'IP \K[0-9.]+(?=\.)')
        
        # JSON verisini parse et
        DATA=$(echo $line | grep -oP 'GET /\K[^\ ]+' | urldecode)
        
        # Terminal çıktısı
        echo -e "\n${GREEN}[YENİ TIKLANMA]${NC}"
        echo -e "${YELLOW}Zaman:${NC} $TIMESTAMP"
        echo -e "${YELLOW}IP Adresi:${NC} $SOURCE_IP"
        echo -e "${YELLOW}Detaylar:${NC}\n$DATA"
        echo -e "${BLUE}----------------------------------------${NC}"
        
        # Log dosyasına kaydet
        echo "[$TIMESTAMP] IP: $SOURCE_IP | Data: $DATA" >> "$LOG_FILE"
        
        # HTML'e ekle
        cat >> "$HTML_LOG" << EOF
        <div class="click">
            <div class="timestamp">$TIMESTAMP</div>
            <div class="ip">IP: $SOURCE_IP</div>
            <div class="details">$DATA</div>
        </div>
EOF
    fi
done

# Ctrl+C ile çıkışta HTML'i tamamla
trap 'echo "</div></body></html>" >> "$HTML_LOG"' EXIT
