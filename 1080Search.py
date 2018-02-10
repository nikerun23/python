import requests
from bs4 import BeautifulSoup as bs

req = requests.get('http://www.coolenjoy.net/bbs/jirum')
html = req.text

soup = bs(html, 'lxml')
melonChartList = soup.select(
    '#fboardlist td.td_subject > a'
)

findText = '1080'
for i in melonChartList :
    resultText = ''.join(i.text.split())
    if resultText.find(findText) > -1:
        print(resultText)
        print('----------------------------')


