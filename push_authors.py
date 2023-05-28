import pymongo
import json
from pymongo import InsertOne

client = pymongo.MongoClient("mongodb+srv://ruslan:qwerty123@cluster.9diyzhg.mongodb.net/?retryWrites=true&w=majority")
db = client.test
collection = db.authors
requesting = []

with open("authors.json", "r") as f:
    myDict = json.load(f)
    for i in myDict:
        requesting.append(InsertOne(i))

result = collection.bulk_write(requesting)
client.close()
