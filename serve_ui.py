import http.server
import socketserver
import os

# Set the directory to serve files from
web_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(web_dir)

# Configure the server
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

print(f"Starting server at http://localhost:{PORT}")
print(f"Open this URL in your browser to view the UI: http://localhost:{PORT}/ui.html")
print("Press Ctrl+C to stop the server")

# Start the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")