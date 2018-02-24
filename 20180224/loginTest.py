import requests

s = requests.Session()
dic = {
    'myName' : 'hyunkeun',
    'pw' : 'qwer'
}

res = s.post('http://httpbin.org/post', data=dic)
print(res.json())