import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.inflearn.com/wp-login.php'

s = requests.Session() # Session 객체 생성

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'referer': 'https://www.inflearn.com/wp-login.php'
}
s.headers = headers # Session 객체에 헤더 추가

s.post(url, data={'log': 'nikerun23',
                  'pwd': 'wlsldjtm23'
                  }
       )

res = s.get('https://www.inflearn.com/')
soup = bs(res.text, 'lxml')
name = soup.select_one('ul.topmenu > li:nth-of-type(1) > a > span')
print(name.text)