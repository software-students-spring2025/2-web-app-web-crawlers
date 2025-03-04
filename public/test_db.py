import pymongo
import os
import datetime
from dotenv import load_dotenv
from bson.objectid import ObjectId
from db import connectDB, insert, search, update, delete, display

def test_db():
    print("\nRunning Database Tests...\n")

    client = connectDB()
    db = client["project2_db"]
    collection = db["testCollection"]

    test_document = {
        "name": "Test User",
        "email": "test@example.com",
        "created_at": datetime.datetime.utcnow()
    }

    print("\n📌 Inserting Test Document...")
    inserted_id = insert(collection, test_document)
    print(f"✅ Inserted Document ID: {inserted_id}")

    print("\n📌 Searching for Test Document...")
    found_docs = search(collection, {"_id": inserted_id})
    if found_docs:
        print(f"✅ Found Document: {found_docs[0]}")
    else:
        print("❌ Document not found!")

    print("\n📌 Updating Test Document...")
    update_count, modified_count = update(collection, {"_id": inserted_id}, {"email": "updated@example.com"})
    if modified_count > 0:
        print(f"✅ Document updated successfully: {modified_count} changes made.")
    else:
        print("❌ No changes were made.")

    print("\n📌 Searching for Updated Document...")
    updated_doc = search(collection, {"_id": inserted_id})
    if updated_doc and updated_doc[0]["email"] == "updated@example.com":
        print(f"✅ Email updated successfully: {updated_doc[0]['email']}")
    else:
        print("❌ Email update failed!")

    print("\n📌 Deleting Test Document...")
    deleted_count = delete(collection, {"_id": inserted_id})
    if deleted_count > 0:
        print("✅ Document deleted successfully.")
    else:
        print("❌ Document deletion failed.")

    print("\n📌 Verifying Deletion...")
    deleted_doc = search(collection, {"_id": inserted_id})
    if not deleted_doc:
        print("✅ Document successfully removed from database.")
    else:
        print("❌ Document still exists!")

    print("\n🎉 All Database Tests Completed!\n")

if __name__ == "__main__":
    test_db()
