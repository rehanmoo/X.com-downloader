#!/usr/bin/env python3
import os
import json
import time
import subprocess
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

# Configuration
DOWNLOAD_DIR = os.path.expanduser("~/Downloads/x_videos")
PORT = 8765

# Create download directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class VideoDownloadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)
        
        video_url = data.get('url')
        if video_url and ('x.com' in video_url or 'twitter.com' in video_url):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Start download in a separate thread to avoid blocking
            self.download_video(video_url)
            
            response = {'status': 'downloading', 'url': video_url}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {'status': 'error', 'message': 'Invalid URL'}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def download_video(self, url):
        try:
            print(f"Downloading video from: {url}")
            subprocess.Popen([
                'yt-dlp', 
                '--no-warnings',
                '-o', f'{DOWNLOAD_DIR}/%(title)s-%(id)s.%(ext)s',
                url
            ])
            print(f"Download started for {url}")
        except Exception as e:
            print(f"Error downloading video: {e}")

def run_server():
    handler = VideoDownloadHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print(f"Videos will be saved to {DOWNLOAD_DIR}")
        print("Waiting for X.com videos to be played...")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
