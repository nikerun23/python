import csv

src = 'csv/url_list.csv'
csv_reader = csv.DictReader(open(src, encoding='UTF8'))

url_field_names = csv_reader.fieldnames
url_dict_list = []

print(url_field_names)
for index, h in enumerate(url_field_names):
    print(index,h)

for row in csv_reader.reader:
    urlDict = {}
    if 'X' == row[7]: # Crawler
        continue
    for index, h in enumerate(url_field_names):
        urlDict[h] = row[index].strip()
    url_dict_list.append(urlDict)

print(len(url_dict_list))
print(url_dict_list)
print(url_dict_list[71]['URL'])
