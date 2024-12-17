from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PWD = os.getenv("MONGO_PWD")
CLUSTER = os.getenv("CLUSTER")
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PWD}@{CLUSTER}.mnhm7.mongodb.net/?retryWrites=true&w=majority&appName={CLUSTER}"
DB_NAME = "housing_data"  

def get_database():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        print("Connected to MongoDB")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
    
