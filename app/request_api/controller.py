from datetime import datetime

from flask import abort

from mongoframes import *
from bson.objectid import ObjectId

from app.util.util import abort_invalid_obj_id
from app.util.util import abort_missing_object_key
# from app.util.firebase_helper import send_topic_push, subscribe_news

from .model import *
from app.models import User, Request, RequestStatus

now: datetime = datetime.now()
CURRENT_TIMESTAMP: str = now.strftime("%d/%m/%Y %H:%M:%S")


def fetch_request(request, current_user):
    abort_missing_object_key('request_no', request)

    abort_invalid_obj_id(current_user['id'])

    req = get_request_by_id(request['request_no'])

    if not req:
        abort(400, description="Not Found, No Request/s is Found.")

    return req


def fetch_all_request(current_user):
    abort_invalid_obj_id(current_user['id'])

    user = User.one(Q._id == ObjectId(current_user['id']), projection={'type': 1})
    user = user.to_json_type()

    # If user is not a delivery.
    if user['type'] not in ('D', 'd'):
        req = Request.many(Q.user_id == ObjectId(current_user['id']), projection={
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
            '_id': 0}, sort=[('create_date', DESC)])

        if not req:
            abort(400, description="Not Found, No Request/s is Found.")

        return [item.to_json_type() for item in req]

    delivery_list = []

    req_status = RequestStatus.many(And(Q.user_id == ObjectId(current_user['id']), Q.status != RequestStatus.StatusDecline),
                                    projection={'request_id': 1, 'status': 1})
    user_req_status = [item.to_json_type() for item in req_status]

    # First: we add all request this delivery user can view.
    for req_item in user_req_status:
        req_id = req_item['request_id']
        req = Request.by_id(ObjectId(req_id),sort={ 'create_date' } ,projection={
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
            '_id': 0})
        if req:
            delivery_list.append(req.to_json_type() | {'status': req_item['status']})

    if not delivery_list:
        abort(400, description="Not Found, No Request/s is Found.")

    return delivery_list


def create_request(request, current_user):
    if not ObjectId.is_valid(current_user['id']):
        abort(400, description=f"Invalid id, '{current_user['id']}' is not a valid ObjectId.")

    user = User.one(Q._id == ObjectId(current_user['id']), projection={'type': 1})
    user = user.to_json_type()

    # If user is not a normal user.
    if user['type'] not in ('U', 'u'):
        abort(400, description="Only User of type User Can create requests.")

    try:
        new_req = Request(
            user_id=ObjectId(current_user['id']),
            user_name=request['user_name'],
            user_phone=request['user_phone'],
            user_address=request['user_address'],
            customer_name=request['customer_name'],
            customer_phone=request['customer_phone'],
            customer_address=request['customer_address'],
            price=request['price'],
            description=request['description'],
            create_date=CURRENT_TIMESTAMP)

        new_req.insert()
    except Exception as e:
        abort(400, description=f"There was an error while inserting new request, {e}.")

    new_req = new_req.to_json_type()
    # subscribe_news()
    # send_topic_push("New Request", f"Request no {new_req['_id']}, price {new_req['price']}, from {new_req['user_address']} to {new_req['customer_address']}")
    return {'msg': 'Created successfully', 'status': 201}


def update_request(request, current_user):
    abort_missing_object_key('request_no', request)

    if not ObjectId.is_valid(request['request_no']):
        abort(400, description=f"Invalid request_no, '{request['id']}' is not a valid ObjectId.")

    req = Request.by_id(ObjectId(request['request_no']))

    if not req:
        abort(400, description=f"Not Found, request_no - '{request['request_no']}' Doesn't Exist.")

    try:
        new_req = Request(
            _id=ObjectId(request['request_no']),
            user_id=ObjectId(current_user['id']),
            user_name=request['user_name'],
            user_phone=request['user_phone'],
            user_address=request['user_address'],
            customer_name=request['customer_name'],
            customer_phone=request['customer_phone'],
            customer_address=request['customer_address'],
            price=request['price'],
            description=request['description'],
            create_date=request['create_date'])

        new_req.update()
    except Exception as e:
        abort(400, description=f"There was an error while updating request, {e} .")

    return {'msg': 'Updated successfully', 'status': 201}


def delete_request(request):
    abort_missing_object_key('request_no', request)

    req = Request.by_id(ObjectId(request['request_no']))

    if not req:
        abort(400, description=f"Not Found, request_no - '{request['request_no']}' Doesn't Exist.")

    req.delete()

    return {'msg': 'Deleted successfully', 'status': 201}


def fetch_all_req(current_user):
    user_id = ObjectId(current_user['id'])
    user = User.one(Q._id == ObjectId(user_id), projection={'type': 1})
    user = user.to_json_type()

    if user['type'] not in ('D', 'd'):
        abort(400, description="Only User of type Delivery (D, d) Can View All Requests.")

    # TODO: If Delivery has more than 5 request cannot accept more

    #: Execlude any accepted / declined requests by the delivery user
    #: Also any accepted status by any other delivery user.
    req_status = RequestStatus.many(Q.user_id == ObjectId(user_id), projection={'request_id': 1, 'status': 1})
    accepted_status = RequestStatus.many(Q.status == 'A', projection={'request_id': 1, 'status': 1})

    no_show_status = []
    if req_status or accepted_status:
        no_show_status = [item.to_json_type() for item in req_status + accepted_status]
        no_show_status = [ObjectId(item['request_id']) for item in no_show_status]

    reqs = Request.many(NotIn(Q._id, no_show_status),projection={
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
        '_id': 0}, sort=[('create_date', DESC)])

    if not reqs:
        abort(400, description="Not Found, No Requests found.")

    return [req.to_json_type() for req in reqs]


class ReqStatus:
    # Todo Refactor The code
    def __init__(self, request: dict, current_user: dict, status: str):
        self.request = request
        self.current_user = current_user
        self.status = status
        self.RequestStatus = status

    # TODO Different Users Cannot accept / decline already accepted requests
    def change_status(self):

        abort_missing_object_key('request_no', self.request)

        user = User.one(Q._id == ObjectId(self.current_user['id']), projection={'type': 1})
        user = user.to_json_type()

        if user['type'] not in ('D', 'd'):
            abort(400, description="Only User of type Delivery (D, d) Can Accept or decline Requests.")

        req = Request.by_id(ObjectId(self.request['request_no']))

        if not req:
            abort(400, description=f"Not Found, request_no - '{self.request['request_no']}' Doesn't Exist.")

        req_status = RequestStatus.one(
            And(Q.request_id == ObjectId(self.request['request_no']), Q.user_id == ObjectId(self.current_user['id'])))

        if req_status:
            req_status.status = self.RequestStatus
            req_status.edit_date = CURRENT_TIMESTAMP
            req_status.update()
        else:
            try:
                new_req_status = RequestStatus(
                    request_id=ObjectId(self.request['request_no']),
                    user_id=ObjectId(self.current_user['id']),
                    status=RequestStatus.StatusAccept,
                    create_date=CURRENT_TIMESTAMP,
                    edit_date=None)

                new_req_status.insert()
            except Exception as e:
                abort(400, description=f"There was an error while inserting new request status, {e} .")

        return {'msg': 'Success', 'status': 200}
