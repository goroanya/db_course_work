import os
import csv

import pymongo
from dotenv import load_dotenv

load_dotenv()


def get_collection():
    client = pymongo.MongoClient(os.getenv('DB_URL'))
    db = client['ads']
    return db['ads']


def backup(mongo_url, filepath):
    if not filepath.endswith('.csv'):
        filepath = filepath + '.csv'
    client = pymongo.MongoClient(mongo_url)
    data = client['ads']['ads'].find()
    with open(filepath, 'w+') as file:
        writer = csv.DictWriter(file, fieldnames=['area', 'number_of_rooms', 'price', 'region', 'source'])
        writer.writeheader()
        for ad in data:
            del ad['_id']
            writer.writerow(ad)


def restore(mongo_url, filepath):
    client = pymongo.MongoClient(mongo_url)
    collection = client['ads']['ads']
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            collection.insert(row)
