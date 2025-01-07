from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import yt_dlp

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        query = parse_qs(self.path[2:])  # Récupération des paramètres dans l'URL
        video_url = query.get('url', [None])[0]
        
        if not video_url:
            self.wfile.write("Veuillez fournir une URL YouTube".encode('utf-8'))
            return

        ydl_opts = {
            'format': 'best',
            'outtmpl': '/tmp/%(title)s.%(ext)s',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_file = ydl.prepare_filename(info)

            self.wfile.write(f"Vidéo téléchargée avec succès : {video_file}".encode('utf-8'))
        except Exception as e:
            self.wfile.write(f"Erreur : {str(e)}".encode('utf-8'))
