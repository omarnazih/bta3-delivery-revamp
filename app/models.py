from mongoframes import *
from pymongo import MongoClient

# Connect MongoFrames to the database
Frame._client = MongoClient('mongodb+srv://admin:42F7iDLNt002Xagy@cluster0.wffxo.mongodb.net/bta3-delivery?retryWrites=true&w=majority')


class User(Frame):
    _fields = {
        'name',
        'password',
        'mobile',
        'picture',
        'id_image',
        'type',
    }


class Request(Frame):
    _fields = {
        'user_id',
        'user_name',
        'user_phone',
        'user_address',
        'customer_name',
        'customer_phone',
        'customer_address',
        'price',
        'description',
        'create_date'
    }


class RequestStatus(Frame):
    _fields = {
        'request_id',
        'user_id',
        'status',
        'create_date',
        'edit_date'
    }

    StatusAccept = 'A'
    StatusDecline = 'D'


class HelpRequests(Frame):
    _fields={
        'message',
        'name',
        'phone',
        'time_frame'
    }
