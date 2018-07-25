import requests
from bs4 import BeautifulSoup as bs


headers = {
    'Origin': 'http://www.ntis.go.kr',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://www.ntis.go.kr/ThMain.do',
    'Connection': 'keep-alive',
}

data = [
  ('uurl', 'http://www.ntis.go.kr/ThMain.do'),
  ('userid', 'hoon1234'),
  ('password', 'gate4fkd!!'),
]

ss = requests.Session()
ss.headers = headers
ss.get('http://www.ntis.go.kr/ThMain.do')
# print(req.text)

# ss.post('http://www.ntis.go.kr/ThMainIdCheck.do?userId=hoon1234&password=gate4fkd!!', data=data)
# ss.post('http://www.ntis.go.kr/ThMainPwdCheck.do?userId=hoon1234&password=gate4fkd!!', data=data)
# ss.post('https://sso2.ntis.go.kr/3rdParty/mobile/ssoLogin.jsp', data=data)
ss.post('https://sso2.ntis.go.kr/3rdParty/mobile/ssoLogin.jsp?userid=hoon1234&password=gate4fkd!!', data=data)
req = ss.get('http://www.ntis.go.kr/ThMain.do')
print(req.text)
soup = bs(req.text, 'lxml')
login = soup.select_one('body > div.main_container_wrap > div.mainbox1 > div.aside > div.userinfogroup')
print(login.text)

data = [
  ('waUid', ''),
  ('waBbsUid', ''),
  ('confirmYn', 'Y'),
  ('roFormCd', '28802'),
  ('deptCd', 'P50'),
  ('wcCompanyName', 'TEST부처명'),
  ('wcTitle', 'TEST제목'),
  ('wcUrl', 'TESTURL'),
  ('wcDt', '2018-03-14'),
  ('roStrtDt', '2018-03-15'),
  ('roEndDt', '2018-03-17'),
  ('roDivCd', ''),
  ('roAmt', ''),
  ('hour', '00'),
  ('min', '00'),
  ('roReference', ''),
  ('roDbrainCd', ''),
  ('wcPContent', 'TEST내용'),
  ('', ''),
]
# response = requests.post('http://www.ntis.go.kr/rndgate/eg/un/ra/create.do', headers=headers, data=data)

# print(response.status_code)