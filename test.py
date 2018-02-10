file = open('testfile.txt', 'w+')
file.write('New Text Line...')
file.writelines(
    [
        '여러줄을\n',
        '쓸꺼에요\n',
        '블라블라'
    ]
)
file.close()