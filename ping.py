# pdf_listener.py
import http.server
import socketserver
from datetime import datetime
import os

# Log dosyası yolu
LOG_DIR = "/root/pdf_pings"
LOG_FILE = os.path.join(LOG_DIR, "pdf_pings.log")

# Dizin ve log dosyası kontrolü
def setup_logging():
    # Dizin yoksa oluştur
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # Log dosyası yoksa oluştur
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'a').close()
    
    print(f"Log dosyası: {LOG_FILE}")

class PingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # CORS headerları
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        # Zaman damgası
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # İstemci IP'si
        client_ip = self.client_address[0]
        
        # Log mesajı
        log_message = f"[{timestamp}] PDF Açıldı! | IP: {client_ip} | Path: {self.path}\n"
        
        # Ekrana yazdır
        print("\n" + "="*50)
        print("PDF AÇILDI!")
        print("="*50)
        print(log_message)
        
        # Dosyaya kaydet
        try:
            with open(LOG_FILE, "a") as f:
                f.write(log_message)
        except Exception as e:
            print(f"Log yazma hatası: {e}")

def main():
    # Log sistemi kur
    setup_logging()
    
    # Sunucu ayarları
    port = 8765
    handler = PingHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"PDF ping sunucusu başlatıldı - Port: {port}")
            print(f"Log dosyası: {LOG_FILE}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Sunucu hatası: {e}")

if __name__ == "__main__":
    main()
