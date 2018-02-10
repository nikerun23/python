file3 = open('testfile.txt', 'r')
print('## 파일 한번에 모두 출력하기 ##')
print(file3.read())

file3.close()

file2 = open('testfile.txt')

print('## 파일 한줄씩 출력하기 ##')
for line in file2.readlines():
    print(line)

file2.close()
