import datetime


dateTemp = '2017.01. 1.'
dateTemp = dateTemp.replace(' ', '').replace(',', '-').replace('.', '-')
print(dateTemp)
if dateTemp[-1] == '-':
    dateTemp = dateTemp[:-1]
print(dateTemp)

dateTimeStr = datetime.datetime.strptime(dateTemp, '%Y-%m-%d')
dateType = datetime.date(dateTimeStr.year, dateTimeStr.month, dateTimeStr.day)
print(dateType)