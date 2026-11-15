"""Explicitly permitted site for local-only integration demo."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

class FixtureHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        b=b'<html><head><title>VersionVault fixture</title></head><body style="font:24px system-ui"><h1>VersionVault controlled test website</h1><p>Change this text and capture again to compare versions.</p></body></html>'
        self.send_response(200)
        self.send_header('Content-Type','text/html')
        self.send_header('Content-Length',str(len(b)))
        self.end_headers()
        self.wfile.write(b)

if __name__=='__main__':
    print('Fixture on http://127.0.0.1:8766/')
    ThreadingHTTPServer(('127.0.0.1',8766),FixtureHandler).serve_forever()
