from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://nikshub175:0Mj5PCRYSeP3S8OF@githubprofile.nxnnjhg.mongodb.net/?retryWrites=true&w=majority&appName=Githubprofile"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
