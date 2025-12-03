import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("mongodb://localhost:27017/"))
db = client.smartkisan
users = db.users
