import requests

print requests.post("http://localhost:8080/hello", headers={'authorization': 'dummy-auth-token'}, json={'input': 'data'}).json()
