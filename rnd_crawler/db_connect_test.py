import cx_Oracle

conn = cx_Oracle.connect('state_dev/dhQkWkd8@112.216.140.126:1522/orcl')
print(conn)
cursor = conn.cursor()
print(cursor)

# sql = "select * from TCO_MENUINFO where MENU_NO LIKE 'A010101%'"
sql = "select count(*) from TCO_MENUINFO"
cursor.execute(sql)
count = cursor.fetchone()

print(count[0])

# items = [(1,2,3,4,5),(1,2,3,4,5)]
# for row in items:
#     sql = "insert into 테이블명 values (:1,:2,:3,:4,:5)"
#     cursor.execute(sql. row)

