import requests

SERVER_URL = 'http://127.0.0.1:5000/'


class DataCollectorsPipeline:
    def process_item(self, item, spider):
        requests.post(f'{SERVER_URL}/ad', json=item)
