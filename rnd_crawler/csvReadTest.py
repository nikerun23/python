import csv

csv_reader = csv.DictReader(open('csv/url_list.csv', encoding='UTF8'))
print(csv_reader.fieldnames)

for index, h in enumerate(csv_reader.fieldnames):
    print(index,h)

for row in csv_reader.reader:
    print(row[2])