from pymongo import MongoClient

client = MongoClient('mongodb://leehk:wlsldjtm23@ds056009.mlab.com:56009/crawler2')
db = client['crawler2']
collection = db['test-collection']

# 컬렉션 전체 인쇄하기
for dic in collection.find():
    print(dic)

client.close()