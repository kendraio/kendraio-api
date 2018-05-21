#!/usr/bin/python
import kendraio_api_server, json, hashlib, sys, time

if __name__ == '__main__':
    def hello_handler(subject, x, context):
        return ("Hello %s! You sent me this:" % subject, x)

    server = kendraio_api_server.api_server("localhost", 8080)

    # load credentials from stdin
    server.add_credentials(json.loads(sys.stdin.read()))
    server.add_handler('/hello', hello_handler)
    server.run()

