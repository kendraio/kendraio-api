import BaseHTTPServer, json

# TO DO: the handlers table is currently a global object: should make this
#        per-instance for each server object

def do_CORS(s):
    s.send_header("Access-Control-Allow-Origin", "*")
    s.send_header("Access-Control-Allow-Headers", "*")

def send_error(s, err_code, err_message):
    s.send_response(err_code)
    do_CORS(s)
    s.send_header("Content-type", "application/json")
    s.end_headers()
    s.wfile.write(json.dumps({"error": err_code, "details": err_message}))

def handle_POST(s):
    global handlers
    try:
        content_length = int(s.headers['Content-Length'])
        request = json.loads(s.rfile.read(content_length))
    except:
        return send_error(s, 500, "can't parse request body")
    
    if s.path not in handlers:
        return send_error(s, 404, "no handler for request path")        

    try:
        response = handlers[s.path](request)
    except:
        return send_error(s, 500, "request handler threw exception")

    try:
        response_data = json.dumps(response)
    except:
        return send_error(s, 500, "can't format response as JSON")
        
    s.send_response(200)
    do_CORS(s)
    s.send_header("Content-type", "application/json")
    s.end_headers()
    s.wfile.write(response_data)

        
class request_handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        send_error(s, 404, "can't handle HEAD requests")

    def do_GET(s):
        send_error(s, 404, "can't handle GET requests")

    def do_UPDATE(s):
        send_error(s, 404, "can't handle UPDATE requests")

    def do_DELETE(s):
        send_error(s, 404, "can't handle DELETE requests")

    def do_OPTIONS(s):
        s.send_response(200)
        do_CORS(s)
        s.send_header("Content-type", "application/json")

    def do_POST(s):
        handle_POST(s)

class api_server():
    def __init__(self, hostname, port):
        global handlers
        self.httpd = BaseHTTPServer.HTTPServer((hostname, port), request_handler)
        handlers = {}
        
    def add_handler(self, path, handler):
        global handlers
        handlers[path] = handler

    def remove_handler(self, path):
        global handlers
        if path in handlers:
            del handlers[path]
        
    def run(self):
        self.httpd.serve_forever()

if __name__ == '__main__':
    def hello_handler(x):
        return ("Hello! You sent me this:", x)
    
    server = api_server("localhost", 8080)
    server.add_handler('/hello', hello_handler)
    server.run()

