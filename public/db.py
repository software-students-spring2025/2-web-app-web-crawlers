import pymongo  
import time
import datetime
import platform

def connectDB():
    # User name:lgl1876523678
    # Password: 1017
    client = pymongo.MongoClient("mongodb+srv://lgl1876523678:1017@cluster0.k8xwe.mongodb.net/?retryWrites=true&w=majority")
    return client

def insert(collection, doc):
    print("\n*** Insert an Item")
    return collection.insert_one(doc).inserted_id
    
def search(collection, filter_dict):
    print("\n*** Search for an Item")
    return list(collection.find(filter_dict))

    
def update(collection, filter_dict, update_dict):
    result = collection.update_one(filter_dict, update_dict)
    matched = result.matched_count     
    modified = result.modified_count    
    print(f"\n*** Update - Matched: {matched}, Modified: {modified}")
    return result.matched_count, result.modified_count

def display(collection):
    print("\n*** Display All Documents in collection:")
    return list(collection.find())
    
def delete(collection, filter_dict):
    result = collection.delete_one(filter_dict)
    deleted_count = result.deleted_count
    print(f"\n*** Deleted documents: {deleted_count}")
    return result.deleted_count

def testInfo():
    print("\n")
    seed = "490000514095612094711092719200618300609300923300527300409400454500"
    length = len(seed)

    for i in range(11):
        
        start_index = length - 6 * (i + 1)
        end_index = length - 6 * i
        seed_cup = seed[start_index:end_index]

        sub_seed = int(seed_cup)
      
        for _ in range(3):
            emp = sub_seed % 10   
            sub_seed //= 10       

            print(" " * emp, end="")  

            star = sub_seed % 10    
            sub_seed //= 10

            print("*" * star, end="") 

        time.sleep(0.05)
        print()  
    
    projectName="SWE Project 2"
    db_name="Atlas"
    environment="Testing"
    version="1.0"
    extra_info="Web Crawlers"
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


    