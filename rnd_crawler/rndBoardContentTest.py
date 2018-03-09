
f = open("csv/공고문.hwp", 'r')

lines = f.readlines()

for l in lines:
    print(l)

f.close()