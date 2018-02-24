import requests
from bs4 import BeautifulSoup as bs

# cURL Create
headers = {
    'origin': 'https://www.inflearn.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'cache-control': 'max-age=0',
    'authority': 'www.inflearn.com',
    'referer': 'https://www.inflearn.com/',
}

data = [
  ('log', 'nikerun23'),
  ('pwd', 'wlsldjtm23'),
  ('user-submit', '\uB85C\uADF8\uC778'),
  ('user-cookie', '1'),
]

url = 'https://www.inflearn.com/wp-login.php'

s = requests.Session() # Session 객체 생성

s.headers = headers # Session 객체에 헤더 추가

s.get(url) # 쿠키 채우기용 로그인 페이지 방문

s.post('https://www.inflearn.com/wp-login.php', data=data) # 로그인 POST 요청


# 실제 크롤링할 페이지 방문
res = s.get('https://www.inflearn.com/members/nikerun23/dashboard/')
soup = bs(res.text, 'lxml')
studyList = soup.select('#wplms_course_progress-5 > div > ul > li > strong > a')
print(studyList)

for i in studyList:
    print(i.text)