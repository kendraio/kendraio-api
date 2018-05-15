import BaseHTTPServer, json, os, jwt, string

# Note: the JWT public key needs to be put in an environment variable
# called JWT_PUBLIC_KEY

# If you are using Auth0 as identity provider, you can get this from
# the PEM formatted public key _certificate_ at
#
#  https://YOUR_AUTH0_DOMAIN/.well-known/pem
#
# Then extract the public key and load it into the environment like this:
#
#  export JWT_PUBLIC_KEY=`openssl x509 -pubkey -noout -in your_certificate.pem`
#
# The JWT_AUDIENCE enviroment variable will also need to be set to your
# predefined value.

# A note about Python crypto libraries: "pycrypto" doesn't do enough:
# try installing the "cryptography" library

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
    if s.server.require_authorization:
        try:
            # the JWT will typically be preceded by some other token like 'Bearer' or 'JWT':
            # ignore this, and just take the last token on the line 
            authtoken = string.split(s.headers['Authorization'])[-1]
        except:
            return send_error(s, 500, "missing or malformed authorization token")

        try:
            public_key = os.environ["JWT_PUBLIC_KEY"]
            audience = os.environ["JWT_AUDIENCE"]
        except:
            return send_error(s, 500, "can't fetch validation parameters")

        try:
            jwt.decode(authtoken, public_key, algorithms=['RS256'], audience=audience)
        except Exception as e:
            return send_error(s, 500, "can't validate authorization token: %s" % str(e))
    
    try:
        content_length = int(s.headers['Content-Length'])
        request = json.loads(s.rfile.read(content_length))
    except:
        return send_error(s, 500, "can't parse request body")
    
    if s.path not in s.server.handlers:
        return send_error(s, 404, "no handler for request path")        

    try:
        response = s.server.handlers[s.path](request)
    except:
        return send_error(s, 500, "request handler threw exception")

    try:
        response_data = json.dumps(response)
    except:
        return send_error(s, 500, "can't format response as JSON")
        
    s.send_response(200)
    do_CORS(s)
    s.send_header("Content-type", "application/json")
    s.send_header("Cache-control", "max-age=0")
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
        self.httpd = BaseHTTPServer.HTTPServer((hostname, port), request_handler)
        self.httpd.handlers = {}
        self.httpd.require_authorization = True
        
    def add_handler(self, path, handler):
        self.httpd.handlers[path] = handler

    def remove_handler(self, path):
        if path in self.httpd.handlers:
            del self.httpd.handlers[path]
        
    def run(self):
        self.httpd.serve_forever()

if __name__ == '__main__':
    def hello_handler(x):
        return ("Hello! You sent me this:", x)
    
    server = api_server("localhost", 8080)
    server.add_handler('/hello', hello_handler)
    server.run()

