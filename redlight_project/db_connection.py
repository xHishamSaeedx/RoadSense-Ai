import pymongo 

url = 'mongodb://localhost:27017'
client = pymongo.MongoClient(url)

db = client['test_mongo']
db1 = client['RedLightCross']
db2 = client['NoHelmet']