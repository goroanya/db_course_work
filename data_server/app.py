import os

from flask import Flask, request

import settings
from api_schema import AdSchema
from storage import db_instance


app = Flask(__name__)
db = db_instance(os.getenv('DB_URL'))
ad_schema = AdSchema()


def field_validator(schema):
    def decorator(func):
        def wrapper():
            errors = schema.validate(request.get_json())
            if errors:
                return errors, 400
            return func()
        return wrapper
    return decorator


@app.route('/ad', methods=['POST'])
@field_validator(ad_schema)
def create_advertisement():
    data = request.get_json()
    db.advertisements.insert_one(data)
    return {'success': True}, 200


if __name__ == '__main__':
    app.run(debug=True)
