import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client["project2_db"]  # Ensure this matches the database name in MongoDB
    print(" MongoDB connected successfully!")
    print("Collections:", db.list_collection_names())
except Exception as e:
    print(" MongoDB Connection Error:", e)
