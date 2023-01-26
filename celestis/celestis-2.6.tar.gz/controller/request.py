import os
import re
import importlib.util

def extract_function(contents, path):
    match = re.search(r"urls = (\[.+\])", contents)
    if not match:
        return False
    
    urls_array = eval(match.group(1))

    for url in urls_array:
        if url[0] == path:
            return url[1]

def get_view(project_path, method, path, body, http, cookies):
    urls_file = os.path.join(project_path, "urls.py")

    if not os.path.exists(urls_file):
        return False
    
    with open(urls_file, "r") as f:
        contents = f.read()
    
    function_name = extract_function(contents, path)

    if not function_name:
        return False
    
    views_file = os.path.join(project_path, "views.py")

    if not os.path.exists(views_file):
        return False

    spec = importlib.util.spec_from_file_location("views", str(views_file))
    views_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(views_module)

    view_function = getattr(views_module, function_name)
    request_data = {
        "project": project_path,
        "method": method,
        "http": http,
        "body": body,
        "cookies": cookies
    }

    return view_function(request_data)

def redirect(path, cookies=False):
    response = f"HTTP/1.1 302\nLocation: {path}"

    if cookies:
        cookie_header = "Set-Cookie: "
        for cookie in cookies:
            cookie_header += f"{cookie[0]}={cookie[1]}; "
        
        cookie_header = cookie_header[:-4]

        response += f"\n{cookie_header}"
    
    return response

def get_response(project_path, method, path, body, http, cookies):
    response_content = get_view(project_path, method, path, body, http, cookies)
    http_response = re.search(r"HTTP/1.1 {\d+} ", response_content)

    if http_response:
        return http_response

    if not response_content:
        return "HTTP/1.1 404 Not Found\nContent-Type: text/plain\nContent-Length: 9\n\nNot Found"
    
    return f"HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {len(response_content)}\n\n{response_content}"