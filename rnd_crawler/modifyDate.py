import datetime
from .utility import modify_date

date_str = '''작성일 : 
        26
        18.02
        '''

# 과학기술정보통신부
date_str = date_str.split('\n')
print('date_str split : ',date_str)
dd = date_str[1].strip()
mm = date_str[2].strip()[3:]
yy = date_str[2].strip()[:2]
yyyy = datetime.date.today().strftime('%Y')[:2] + yy
date_str = yyyy + '-' + mm + '-' + dd
print(date_str)


date_fm = 'DD/nYY.MM'
date_str = '''작성일 : 
        26
        18.02
        '''
date_tp = (date_fm, date_str)

modify_date(date_fm, date_str)


#
# dd = date_str[:2]
# print('dd : ',dd)
# date_str = date_str.replace('\n', '')
# today = datetime.date.today()
# yyyy = today[:2]
# yyyy = yyyy + date_str[:2]
# print('yyyy : ',yyyy)
# mm = date_str[3:]
# print('mm : ',mm)
# date_str = yyyy + '-' + mm + '-' + dd
