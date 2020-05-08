import os

import pymongo
from dotenv import load_dotenv

load_dotenv()


def get_collection():
    client = pymongo.MongoClient(os.getenv('DB_URL'))
    db = client[os.getenv('DB_NAME')]

    collection_name = os.getenv('DB_COLLECTION')
    collections = db.list_collection_names()
    if collection_name not in collections:
        db.create_collection(collection_name)

    return db[collection_name]

