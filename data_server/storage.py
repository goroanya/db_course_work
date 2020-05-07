import pymongo


def db_instance(url):
    client = pymongo.MongoClient(url)
    db = client['anya']

    collections = db.list_collection_names()
    if 'ads' not in collections:
        db.create_collection('ads')
    if 'timestamps' not in collections:
        db.create_collection('timestamps')

    return db
