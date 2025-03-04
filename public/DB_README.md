* Database for SWE Project 2
    - Michael Liu 03/03/25

* Database Structure
    - Database
        - userInfo 
        - weightList
        - bmrList

* 5 functions to interact with the database

    1. insert(collection, doc)
        - ex. insert(collection, {"name": "TEST2", "age": "00","sex":"TEST2","weight":"00"})

    2. search(collection, filter_dict)
        - ex. results = search(collection, {"name": "TEST"})
             for item in results:
                 print(item)

    3. update(collection, filter_dict, update_dict)
        - ex.  update(collection, {"name": "TEST2"}, {"$set": {"age": 99}})

    4. display((collection))
        - ex. docs = display(collection)
                 for doc in docs:
                    print(doc)
        
    5. delete(collection, filter_dict)
        - ex.  delete(collection, {"title": "TEST"})
* In oder to Use:

    1. Initiate connection at the begining:  client = connectDB()
    2. Then type in the DB name:             db = client["DBname"] 
    3. Choose the collection you want:       collection = db["collectionName"] 
    4. Terminate the connection at the end:  client.close()

     