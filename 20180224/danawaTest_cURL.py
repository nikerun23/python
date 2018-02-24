import requests
from bs4 import BeautifulSoup as bs

headers = {
    'Origin': 'https://auth.danawa.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://auth.danawa.com/login?url=http%3A%2F%2Fcws.danawa.com%2Fpoint%2Findex.php',
    'Connection': 'keep-alive',
}

data = [
  ('redirectUrl', 'http://cws.danawa.com/point/index.php'),
  ('loginMemberType', 'general'),
  ('id', 'hyunkeun'),
  ('password', 'wlsldjtm23'),
]

s = requests.Session()
s.headers = headers
s.get('https://auth.danawa.com/login')
s.post('https://auth.danawa.com/login', data=data)

res = s.get('http://cws.danawa.com/point/index.php')
res.encoding = 'euc-kr'

soup = bs(res.text, 'lxml')
resultName = soup.select_one('div.user_nickname_area > p > span > strong')
print(resultName.text)

