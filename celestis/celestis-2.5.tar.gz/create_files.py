import os

urls_content = '''# Include your urls in this file
urls = [('/', "home")]
'''

views_content = '''# Include your views in this file
def home(request):
    return "<h1>Homepage</h1>
'''

server_content = '''import socket
import threading
import re
import json
import os
from celestis.controller.request import get_response

port = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("localhost", port))
sock.listen(port)

print(f"Server is running on port {port}")

def format_raw_data(body, type_):
    output = {}
    if "application/json" in type_:
        for item in body:
            result = re.search(r'"(.+)": "(.+)"', item)
            if result is not None:
                output[result.group(1)] = result.group(2)
    
    elif "application/x-www-form-urlencoded" in type_:
        for item in body:
            if "&" in item:
                for pairs in item.split("&"):
                    result = re.search(r'(.+)=(.+)', pairs)
                    if result is not None:
                        output[result.group(1)] = result.group(2)
        
            else:
                result = re.search(r'(.+)=(.+)', item)
                if result is not None:
                    output[result.group(1)] = result.group(2)
    
    elif "form-data" in type_:
        for idx, line in enumerate(body):
            key = re.search(r'Content-Disposition: form-data; name="(.+)"', line)
            if key is not None:
                output[key.group(1)] = body[idx+2].replace("\\r", "")
    
    return output

def extract_body(lines):
    content_type = None
    raw_body = None

    for idx, line in enumerate(lines):
        if line.startswith("Content-Type"):
            content_type = line.split(": ")[1]
        if line.startswith("Content-Length"):
            raw_body = lines[idx:].copy()
            raw_body.pop(0)

    if content_type is None:
        return None

    body = format_raw_data(raw_body, content_type)
    return body

def extract_cookies(lines):
    for line in lines:
        cookie_match = re.search(r"Cookie: (.+)", line)
        if cookie_match:
            raw_cookies = cookie_match.group(1)
            cookies = [(cookie.split("=")[0], cookie.split("=")[1]) for cookie in raw_cookies.split("; ")]

            return cookies

def parse_request(request):
    if request == "":
        return "GET", "/", "HTTP/1.1", None
    
    lines = request.split("\\n")
    method, path, http = lines[0].split(" ")

    body = extract_body(lines)

    cookies = extract_cookies(lines)

    return method, path, http, body, cookies

def handle_client(conn, addr):
    request = conn.recv(1024).decode('utf-8')

    method, path, http, body, cookies = parse_request(request)
    response = get_response(os.getcwd(), method, path, body, http, cookies)
    conn.sendall(response.encode("utf-8"))
    conn.close()

conn = None

try:
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
except:
    sock.close()
    if conn is not None:
        conn.close()
    
    print("Server has been closed")
    exit()
'''

def create_project_files(project_name):
    os.makedirs(project_name, exist_ok=True)
    
    urls_path = os.path.join(project_name, "urls.py")
    with open(urls_path, "w") as f:
        f.write(urls_content)

    views_path = os.path.join(project_name, "views.py")
    with open(views_path, "w") as f:
        f.write(views_content)
    
    server_path = os.path.join(project_name, "server.py")
    with open(server_path, "w") as f:
        f.write(server_content)
