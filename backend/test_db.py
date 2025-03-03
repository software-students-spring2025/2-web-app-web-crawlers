# main.py
from db import connectDB, insert, display, search,delete,update,testInfo

def main():
    
    client = connectDB()
    db = client["test_db"] # Our DB name: project2_db

    collection = db["testCollection"] # Collection1 name: userInfo
    collection2= db["testCollection2"] # Collection1 name: weightList
    collection3= db["testCollection3"] # Collection1 name: bmrList
    
    testInfo()

    # Insert
    insert(collection2, {"name": "TEST2", "age": "00","sex":"TEST2","weight":"00"})
    insert(collection3, {"name": "TEST3", "age": "00","sex":"TEST3","weight":"00"})
    
    # Search
    results = search(collection, {"name": "TEST"})
    for item in results:
        print(item)
    
    # Update
    update(collection, {"name": "TEST2"}, {"$set": {"age": 99}})
   

    # Delete
    delete(collection, {"title": "TEST"})
   

    # Display All
    docs = display(collection)
    for doc in docs:
        print(doc)

    #client.close()

if __name__ == "__main__":
    main()