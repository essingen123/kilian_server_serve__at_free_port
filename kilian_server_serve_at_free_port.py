import os
import socket
import webbrowser
import subprocess

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def start_server(port, server_type):
    if server_type == "http":
        from http.server import SimpleHTTPRequestHandler, HTTPServer
#        os.chdir(os.path.dirname(__file__))
        os.chdir(os.getcwd())
        httpd = HTTPServer(("localhost", port), SimpleHTTPRequestHandler)
        print(f"Serving on port {port} with HTTPServer...")
        try:
            while True:
                httpd.handle_request()
        except KeyboardInterrupt:
            print("\nServer stopped.")
    elif server_type == "flask":
        from flask import Flask, send_from_directory
        app = Flask(__name__)
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve(path):
            return send_from_directory('.', path)
        app.run(port=port)
        print(f"Serving on port {port} with Flask...")
    elif server_type == "nginx":
        os.system(f"nginx -c nginx.conf -p . &")
        print(f"Serving on port {port} with Nginx...")
    elif server_type == "lighttpd":
        os.system(f"lighttpd -D -f lighttpd.conf -p {port} &")
        print(f"Serving on port {port} with Lighttpd...")
    elif server_type == "twistd":
        from twisted.web.server import Site
        from twisted.web.wsgi import WSGIResource
        from twisted.internet import reactor
        from twisted.python.threadpool import ThreadPool
        resource = WSGIResource(reactor, ThreadPool(minThreads=1, maxThreads=100), lambda: None)
        site = Site(resource)
        reactor.listenTCP(port, site)
        reactor.run()
        print(f"Serving on port {port} with Twistd...")
    else:
        print("Invalid server type. Exiting.")
        return

import sys

def open_in_browser(port):
    url = f"http://localhost:{port}"
    print(f"Opening {url} in browser...")
    webbrowser.open(url, new=2)
    if sys.platform == 'darwin':  # macOS
        subprocess.run(['open', url])
    elif sys.platform == 'win32':  # Windows
        subprocess.run(['start', url], shell=True)
    else:  # Linux
        subprocess.run(['xdg-open', url])


def print_instructions(port):
    print(f"Server started. Access your webpage at http://localhost:{port}")
    print("Press Ctrl+C to stop the server (except for Nginx and Lighttpd).")

def the_runner():
    print("Choose a server type:")
    print("1. HTTPServer")
    print("2. Flask")
    print("3. Nginx")
    print("4. Lighttpd")
    print("5. Twistd")
    choice = input("Enter the number of your choice: ")
    server_type = {
        "1": "http",
        "2": "flask",
        "3": "nginx",
        "4": "lighttpd",
        "5": "twistd"
    }.get(choice, "Invalid choice")
    if server_type == "Invalid choice":
        print("Invalid choice. Exiting.")
        return
    port = find_free_port()
    print_instructions(port)
    # if server_type != "nginx" and server_type != "lighttpd":
    #     open_in_browser(port)
    open_in_browser(port)

    start_server(port, server_type)

if __name__ == "__main__":
    the_runner()