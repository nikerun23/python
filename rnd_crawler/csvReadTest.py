import csv

csv_reader = csv.DictReader(open('csv/url_list.csv', encoding='UTF8'))

urlFieldNames = csv_reader.fieldnames
urlDicList = []
urlDic = {}

print(urlFieldNames)
for index, h in enumerate(urlFieldNames):
    print(index,h)

for row in csv_reader.reader:
    for index, h in enumerate(urlFieldNames):
        urlDic[h] = row[index]

    urlDicList.append(urlDic)

print(len(urlDicList))
print(urlDicList[7])