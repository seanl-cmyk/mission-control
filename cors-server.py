#!/usr/bin/env python3
"""Simple HTTP server with CORS enabled for Mission Control status."""
import http.server
import os

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    os.chdir('/home/telnyx-user/mission-control')
    server = http.server.HTTPServer(('0.0.0.0', 8081), CORSRequestHandler)
    print('🎯 Mission Control Status Server running on port 8081 (CORS enabled)')
    server.serve_forever()
