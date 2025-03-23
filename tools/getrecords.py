from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://sai444134:1234567899@cluster0.6nyzm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Select the database and collection
db = client['test']
collection = db['users']

# Find all documents in the collection
documents = collection.find()
# Print the documents
for document in documents:
    print(document['username'])
print("users Count=",collection.count_documents({}))

# Close the MongoDB connection
client.close()
