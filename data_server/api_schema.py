from marshmallow import Schema, fields


class AdSchema(Schema):
    """ /ad - POST

    Parameters:
     - number_of_rooms (int)
     - area (int)
     - price (int)
     - region (str)
     - address (str)
     - source (str)
    """
    number_of_rooms = fields.Int(required=True)
    area = fields.Int(required=True)
    price = fields.Int(required=True)
    region = fields.Str(required=True)
    address = fields.Str()
    source = fields.Str()
