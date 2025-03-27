print("Questions wrapper imported!")


from fastapi import Query
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb://localhost:27017/"

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "QuestionsRepo"

import json

with open('config.json') as f:
    config = json.load(f)
questionsUri = config['mongodb']['repositories']['QuestionsRepo']['con_str']
dbName=config['mongodb']['repositories']['QuestionsRepo']['database_name']
# Create a MongoDB client
client = AsyncIOMotorClient(questionsUri)

# Get a reference to the database
db = client[dbName]
async def get_questions(ids: list = Query(...)):
    #ids = [int(id) for id in ids[0].split(",")]
    questions_collection = db["Questions"]
    count = await questions_collection.count_documents({})
    #print(count)
    questions = {}
    keys = []
    for id in ids:
        q=await questions_collection.find_one({"_id":id})
        #print(q["Key"])
        keys.append(q["Key"])
        del q["Key"];del q["id"]
        #q["Q"][0] = "TemporarilyMasked"
        questions[id]=q
    #questions = await questions_collection.find({"_id": {"$in": ids}}).to_list(None)

    return questions,keys

async def saveUserTopics(userid:str, payload: dict):
    userTopicsCollection = db["UserTopics"] #contains useremail(key) vs selected topics metadata(value)
    #await userTopicsCollection.insert_one(payload)
    await userTopicsCollection.update_one({"_id": userid}, {"$set": payload}, upsert=True)
    print(f"user topics saved successfully for {userid}")
    pass
