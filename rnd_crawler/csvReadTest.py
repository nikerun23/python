import csv

src = 'csv/url_list.csv'
csv_reader = csv.DictReader(open(src, encoding='UTF8'))

urlFieldNames = csv_reader.fieldnames
urlDictList = []

print(urlFieldNames)
for index, h in enumerate(urlFieldNames):
    print(index,h)

for row in csv_reader.reader:
    urlDict = {}
    if 'X' == row[7]: # Crawler
        continue
    for index, h in enumerate(urlFieldNames):
        urlDict[h] = row[index].strip()
    urlDictList.append(urlDict)

print(len(urlDictList))
print(urlDictList)
print(urlDictList[71]['URL'])
