from app.models import (Request, RequestStatus)

from bson.objectid import ObjectId

def get_request_by_id(request_id: int) -> dict:
    return Request.by_id(
            ObjectId(request_id),
            projection={
            'request_no': {"$toString": "$_id"},
            'user_name': 1,
            'user_phone': 1,
            'user_address': 1,
            'customer_name': 1,
            'customer_phone': 1,
            'customer_address': 1,
            'description': 1,
            'create_date': 1,
            'price': 1,
            '_id': 0}
            ).to_json_type()