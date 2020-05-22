import storage


class DataCollectorsPipeline:
    collection = storage.get_collection()

    def process_item(self, item, spider):
        self.collection.insert_many(item['data'])
        return item['data']
