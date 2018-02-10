import requests

req = requests.get('http://naver.com')

print(req.headers)
print(req.url)
print(req.ok)
print(req.history)
print(req.encoding)
print(req.status_code)
