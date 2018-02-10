import requests
from bs4 import BeautifulSoup as bs

req = requests.get('http://jtbc.joins.com/schedule?cloc=jtbc|header|guide')
html = req.text

soup = bs(html, 'lxml')
jtbcList = soup.select(
    'ul.chart_time_list > li > div.prg_title_table > strong.title'
)

for i in jtbcList:
    resultTtext = ''.join(i.text.split())
    print(resultTtext)
    print('--------------------')
