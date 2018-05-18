import kendraio_api_server, json, hashlib, sys, time

if __name__ == '__main__':
    def hello_handler(subject, x):
        return ("Hello %s! You sent me this:" % subject, x)

    def assert_handler(source_id, statement):
        # Hash a canonical representation of the JSON object
        hash = hashlib.sha256(json.dumps(statement, sort_keys=True)).hexdigest()
        assertion = { 
            "source_id": source_id,
            "timestamp_received": time.time(),
            "statement": statement,
            "statement-hash": hash
        }
        return {"received": assertion}
    
    server = kendraio_api_server.api_server("localhost", 8080)

    # load credentials from stdin
    server.add_credentials(json.loads(sys.stdin.read()))
    server.add_handler('/hello', hello_handler)
    server.add_handler('/assert', assert_handler)
    server.run()

