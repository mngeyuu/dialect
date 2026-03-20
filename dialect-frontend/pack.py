import http.server
import socketserver
import webbrowser
import os
import threading
import time

PORT = 8000
DIRECTORY = "."  # 当前目录

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def open_browser():
    # 等待服务器启动
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}')

def run_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"服务器运行在 http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # 启动浏览器线程
    threading.Thread(target=open_browser).start()
    # 启动服务器
    run_server()