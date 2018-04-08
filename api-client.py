import requests

print requests.post("http://localhost:8080/hello", json={'input': 'data'}).json()
