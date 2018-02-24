import requests
from bs4 import BeautifulSoup as bs

import requests

headers = {
    'Origin': 'http://www.coolenjoy.net',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://www.coolenjoy.net/',
    'Connection': 'keep-alive',
}

data = [
  ('mb_id', 'hyunkeun'),
  ('mb_password', 'tkanf'),
]

ss = requests.Session() # Session 객체에 헤더 추가
ss.get('http://www.coolenjoy.net/') # 쿠키 채우기용 로그인 페이지 방문
ss.headers = headers # Session 객체에 헤더 추가
loginnResult = ss.post('http://www.coolenjoy.net/login_check', headers=headers, data=data) # 로그인 POST 요청

# 실제 크롤링할 페이지 방문
res = ss.get('http://www.coolenjoy.net/bbs/mart2') # 회원장터 <Response객체로 반환>

soup = bs(res.text, 'lxml')

tradeList = soup.select('div.tbl_wrap table > tbody > tr > td.td_subject')

findList = '960'

for i in tradeList:
    if findList in i.text:
        print(i.text)

