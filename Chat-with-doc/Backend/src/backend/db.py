from pymongo import MongoClient

client = MongoClient("mongodb+srv://gokulsureshkumar450_db_user:gokultest@cluster0.yitgjka.mongodb.net/?appName=Cluster0")
db = client["chat-with-doc"]
collection = db["data_source"]

'''data = [
    {"title": "Test doc 1", "content": "Hello from MongoDB"},
    {"title": "Test doc 2", "content": "Connection check"},
]

result = collection.insert_many(data)
print("Inserted ids:", result.inserted_ids)'''