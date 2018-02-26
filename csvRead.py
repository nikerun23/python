import csv

csv_reader = csv.DictReader(open('csv/url_List.csv', encoding='UTF8'))
print(csv_reader.fieldnames)
for row in csv_reader.reader:
    print(row[0])