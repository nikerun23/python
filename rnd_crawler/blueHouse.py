import requests
from bs4 import BeautifulSoup as bs
import telegram

# 청와대 견학 스케쥴 신청 가능 한 날짜 크롤링 서비스

url = 'https://www1.president.go.kr/cheongwadae/cwdViewing/viewing.php?srh%5Byear%5D=2018&srh%5Bmonth%5D='
month_list = ['07','08','09','10']
message = '청와대 견학 스케쥴'
schedule_list = []

for month in month_list:
    req = requests.get(url + month)
    html = req.text

    select_css = '#table_cal > tbody > tr > td > div > a'
    soup = bs(html, 'lxml')
    result_list = soup.select(select_css)

    for result in result_list:
        schedule_list.append(result.get('title'))
        print(result.get('title'))

# 스케줄이 있을 경우 메세지에 추가
for schedule in schedule_list:
    message = message + '\n' + schedule

# 텔레그램 Bot 메세지 보내기
my_token = '602824143:AAEjqPKSe95ncMH9lDluEKwR_J7BorJUbWE' # 토큰을 변수에 저장합니다.
bot = telegram.Bot(token=my_token) # bot을 선언합니다.
chat_id = bot.getUpdates()[-1].message.chat.id
bot.sendMessage(chat_id=chat_id, text=message)
