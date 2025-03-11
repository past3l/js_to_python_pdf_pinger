# pdf_listener.py
import http.server
import socketserver
from datetime import datetime
import os

# Log dosyası yolu
LOG_FILE = "/root/pdf_pings/pdf_pings.log"

class PingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # CORS için gerekli headerlar
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        # Zaman damgası
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # İstemci IP'si
        client_ip = self.client_address[0]
        
        # Log mesajı
        log_message = f"[{timestamp}] PDF Açıldı! | IP: {client_ip} | User-Agent: {self.headers.get('User-Agent')}\n"
        
        # Ekrana yazdır
        print("\n" + "="*50)
        print("PDF AÇILDI!")
        print("="*50)
        print(log_message)
        
        # Dosyaya kaydet
        with open(LOG_FILE, "a") as f:
            f.write(log_message)

# Dizin oluştur
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Sunucuyu başlat
port = 8765
with socketserver.TCPServer(("", port), PingHandler) as httpd:
    print(f"PDF ping sunucusu başlatıldı - Port: {port}")
    print(f"Log dosyası: {LOG_FILE}")
    httpd.serve_forever()
