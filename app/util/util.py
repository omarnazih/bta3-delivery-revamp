from flask import abort
from datetime import datetime
from bson.objectid import ObjectId

def abort_missing_object_key(key: str, object: dict) -> None:
    if key not in object:
      abort(400, description=f"missing '{key}' from request object.")


def abort_missing_object_keys(keys: list, object: dict) -> None:
    for key in keys:
      abort_missing_object_key(key, object)


def abort_invalid_obj_id(obj_id: str) -> None:
    if not ObjectId.is_valid(obj_id):
      abort(400, description = f"Invalid id, '{obj_id}' is not a valid ObjectId.")


def get_current_timestamp():
    now: datetime = datetime.now()
    CURRENT_TIMESTAMP: str = now.strftime("%d/%m/%Y %H:%M:%S")
    return CURRENT_TIMESTAMP