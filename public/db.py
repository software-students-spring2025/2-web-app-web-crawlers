import pymongo
import os
from dotenv import load_dotenv

def connectDB():
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise ValueError("Missing MongoDB URI! Check your .env file.")

    client = pymongo.MongoClient(mongo_uri)
    print("\n✅ Successfully connected to MongoDB.")
    return client

def insert(collection, doc):
    print("\n*** Inserting an Item into Collection ***")
    return collection.insert_one(doc).inserted_id
    
def search(collection, filter_dict):
    print("\n*** Searching for Items in Collection ***")
    return list(collection.find(filter_dict))

def update(collection, filter_dict, update_dict):
    if not update_dict.get("$set"):
        update_dict = {"$set": update_dict}

    result = collection.update_one(filter_dict, update_dict)
    print(f"\n*** Update - Matched: {result.matched_count}, Modified: {result.modified_count}")
    return result.matched_count, result.modified_count

def display(collection):
    print("\n*** Displaying All Documents in Collection ***")
    return list(collection.find())

def delete(collection, filter_dict):
    result = collection.delete_one(filter_dict)
    if result.deleted_count == 0:
        print("\n*** No matching document found to delete.")
    else:
        print(f"\n*** Deleted {result.deleted_count} document(s).")
    return result.deleted_count

def testInfo():
    print("\nInitializing Database Connection...\n")

    projectName = "SWE Project 2"
    db_name = "Atlas"
    environment = "Testing"
    version = "1.0"
    extra_info = "Web Crawlers"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info = platform.platform()

    banner = f"""
    -- DATABASE PROGRAM INITIALIZATION --
    
    PROJECT      : {projectName}
    DB NAME      : {db_name}
    ENVIRONMENT  : {environment}
    VERSION      : {version}
    DATE & TIME  : {current_time}
    OS           : {os_info}
    INFO         : {extra_info}
    """
    
    print(banner.strip())
