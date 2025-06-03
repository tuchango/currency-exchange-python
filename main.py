from http.server import HTTPServer

from app.handlers import SimpleHTMLHandler


def run_server(host="localhost", port=8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHTMLHandler)
    print(f"Serving on http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
