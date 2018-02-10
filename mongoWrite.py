from pymongo import MongoClient

client = MongoClient('mongodb://leehk:wlsldjtm23@ds056009.mlab.com:56009/crawler2')
db = client['crawler2']
collection = db['test-collection']

collection.insert_one({
    'id':3,
    'name':'hyunkeun'
})

client.close()