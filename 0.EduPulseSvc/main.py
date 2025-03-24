'''
pip install python-multipart

'''
from functools import wraps
import json
import random
import string
import time
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Query
from pydantic import BaseModel
#from questionsWrapper import get_questions
import questionsWrapper
import testsWrapper
#import questionsWrapper
app = FastAPI()

# MongoDB connection settings
#MONGO_HOST = "localhost"
#MONGO_PORT = 27017
#MONGO_DB = "QuestionsRepo"

import json

with open('config.json') as f:
    config = json.load(f)
questionsUri = config['mongodb']['repositories']['QuestionsRepo']['con_str']
dbName=config['mongodb']['repositories']['QuestionsRepo']['database_name']

# Create a MongoDB client
client = AsyncIOMotorClient(questionsUri)
#client = AsyncIOMotorClient(MONGO_HOST, MONGO_PORT)

# Get a reference to the database
db = client[dbName]

def timer_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"'{func.__name__}' execution time: {execution_time:.2f} ms")
        return result
    return wrapper

@app.get("/")
async def Welcome():
    return "Welcome to Edupulse Microservice!"

@app.get("/topicsMetadata/")
async def get_topics_metadata():
    try:
        topics_metadata_collection = db["SubjectGradeTopicSubtopic"]
        topics_metadata = await topics_metadata_collection.find().to_list(None)
        return topics_metadata
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''
@app.get("/questionsrequestbody/")
async def get_questionsRequestBody(ids: list):
    questions_collection = db["Questions"]
    questions = await questions_collection.find({"_id": {"$in": ids}}).to_list(None)
    return questions

@app.get("/questions/")
async def get_questions(ids: list = Query(...)):
    ids = [int(id) for id in ids[0].split(",")]
    questions_collection = db["Questions"]
    count = await questions_collection.count_documents({})
    #print(count)
    questions = await questions_collection.find({"_id": {"$in": ids}}).to_list(None)
    return questions
'''
class RequestPayload(BaseModel):
    Subject: str = "Physics"
    Grade: list = ["12"]
    Topics: list = ["Mechanics", "Optics"]
    Subtopics: list = ["Rotational motion", "Gravitation", "Mirrors and lenses"]
    Level: list = [9, 10]
    nQuestions: int = 10
    userid: str= "testuser@test.com"


@app.post("/quicktest/")
@timer_decorator
async def create_quick_test(payload: RequestPayload):
    coll_subtopicVsQs = db["subtopic_qids"]
    coll_levelVsQs = db["level_qids"]

    subtopicQs = set()
    for subtopic in payload.Subtopics:
        subtopic_doc = await coll_subtopicVsQs.find_one({"_id": subtopic})
        if subtopic_doc:
            subtopicQs.update(subtopic_doc['qids'])

    levelQs = set()
    for level in payload.Level:
        doc = await coll_levelVsQs.find_one({"_id": level})
        if doc:
            levelQs.update(doc['qids'])
    intersection = subtopicQs & levelQs
    random_ids = random.sample(list(intersection), min(payload.nQuestions, len(intersection)))

    testsWrapper.saveNewTest(payload.userid, {"testQs": list(random_ids),"testKs":list()})
    return {"testQs": list(random_ids)}

@app.get("/quicktest/")
@timer_decorator
async def get_quick_test(useremail: str="testuser@test.com"):
    try: 
        #get the quickTest object for this user containg just Qids and empty keys array.
        quickTest = testsWrapper.getLiveTest(useremail);print(quickTest)
        questions,keys = await questionsWrapper.get_questions(quickTest["testQs"]);#print (questions)
        quickTest["testKs"]=keys;#print(quickTest)
        testsWrapper.saveNewTest(useremail,quickTest)
        return questions
    except Exception as e:
        return {"Error":"No test currently registered"}


'''
TODO APIs:
create_random_test
'''
#uvicorn main:app --reload
#python -m uvicorn main:app --reload
'''
http://localhost:8000/topicsMetadata/
http://localhost:8000/docs
http://localhost:8000/redoc

'''
'''
@app.post("/randomtestv1/")
@timer_decorator
async def create_random_testv1(payload: RequestPayload):
    coll_subtopicVsQs = db["subtopic_qids"]
    coll_levelVsQs = db["level_qids"]
    #print("count of subtopics",(await coll_subtopicVsQs.count_documents({})))
    subtopicQs = []
    levelQs = []
    for subtopic in payload.Subtopics:
        subtopic_doc = await coll_subtopicVsQs.find_one({"_id": subtopic})
        #data = json.dumps(subtopic_doc['qids'])
        if subtopic_doc:
            subtopicQs.extend(subtopic_doc['qids'])
        pass
    #print(subtopicQs)
    #return subtopicQs
    #print("count of qs in subtopic",(await coll_subtopicVsQs.count_documents({})))
    for level in payload.Level:
        doc = await coll_levelVsQs.find_one({"_id": level})
        if doc:
            levelQs.extend(doc['qids'])
        pass
    intersection = list(set(subtopicQs) & set(levelQs))
    #print("count of qs in level",(await coll_levelVsQs.count_documents({})))
    return {"testQs": intersection}
'''