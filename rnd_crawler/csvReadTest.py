import csv

csv_reader = csv.DictReader(open('csv/url_list.csv', encoding='UTF8'))

urlFieldNames = csv_reader.fieldnames
urlDictList = []

print(urlFieldNames)
for index, h in enumerate(urlFieldNames):
    print(index,h)

for row in csv_reader.reader:
    urlDict = {}
    for index, h in enumerate(urlFieldNames):
        urlDict[h] = row[index]
    urlDictList.append(urlDict)

print(len(urlDictList))
print(urlDictList[21])
print(urlDictList[21]['URL'])
