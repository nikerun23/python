import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.inflearn.com/wp-login.php'

s = requests.Session()

s.post(url, data={'log': 'nikerun23',
                  'pwd': '암호'
                  }
       )

res = s.get('https://www.inflearn.com/')
soup = bs(res.text, 'lxml')
name = soup.select_one('ul.topmenu > li:nth-of-type(1) > a > span')
print(name.text)