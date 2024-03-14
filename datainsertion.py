import csv
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
# use this in your powershell in VSCode:$env:MONGODB_URI = "mongodb+srv://nikshub175:0Mj5PCRYSeP3S8OF@githubprofile.nxnnjhg.mongodb.net/?retryWrites=true&w=majority&appName=Githubprofile"
uri = os.environ.get("MONGODB_URI")
if uri is None:
    print("MongoDB URI not found in environment variables.")
    exit()

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def insert_csv_to_mongodb(file_path, collection):
    with open(file_path, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)  
        if not data:
            print("No data found in the CSV file.")
            return
        result = collection.insert_many(data)  
        print("Data inserted successfully. Inserted IDs:", result.inserted_ids)


csv_file_path = "data//file4_converted.csv"  
db = client.get_database("Github_Profiles")
collection = db.get_collection("User_Collection")
insert_csv_to_mongodb(csv_file_path, collection)
