from pymongo import MongoClient

#uri = "mongodb://localhost:27017/"
import json

with open('config.json') as f:
    config = json.load(f)
testsUri = config['mongodb']['repositories']['TestsRepo']['con_str']
dbName=config['mongodb']['repositories']['TestsRepo']['database_name']

# Create a new client
client = MongoClient(testsUri)
testsRepo = client[dbName]

def saveNewTest(user_email, test_json):
    live_tests_collection = testsRepo["LiveTests"]
    live_tests_collection.update_one({"_id": user_email}, {"$set": test_json}, upsert=True)

def getLiveTest(user_email):
    live_tests_collection = testsRepo["LiveTests"]
    #print(testsRepo)
    test_document = live_tests_collection.find_one({"_id": user_email})
    #Note: the find_one above is a O(1) operation, since we are finding for _id. for other fields, it might be O(n)
    if test_document:
        return test_document
    else:
        return {"Error":"No test currently registered"}
    
def submitLiveTest(testResponse):
    pass
