import os
from cloudinary import uploader
from flask import abort
from werkzeug.utils import secure_filename
from mongoframes import *
from bson.objectid import ObjectId

from flask_jwt_extended import create_access_token

from app import app
from app.util.util import abort_missing_object_key
from app.util.util import abort_missing_object_keys

from app.models import User



def fetch_user(current_user):
    if not ObjectId.is_valid(current_user['id']):
        abort(400, description = f"Invalid id, '{current_user['id']}' is not a valid ObjectId.")

    user = User.by_id(ObjectId(current_user['id']), projection={"_id": 0, "password": 0})

    if not user:
        abort(400, description="Not Found, No users is Found.")

    access_token = create_access_token(identity={"name":user['name'], "id":current_user['id']}, fresh=True)

    new_user = user.to_json_type()
    new_user['jwt_user'] = access_token

    new_user['msg'] = 'Created successfully'
    new_user['status'] = 201

    return new_user


def fetch_all_users():
    users = User.many()

    if not users:
        abort(400, description="Not Found, No users found.")

    return [user.to_json_type() for user in users]


def create_user(request):
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    user_type = request.form.get('type')

    picture = request.files['picture']
    id_image = request.files['id_image']

    if not name or not mobile:
        abort(400, description= "Missing Name or Mobile from request Ojbect.")

    if User.one(Q.name == name):
        abort(400, description= f"Duplicate Entry, User - ({name}) already exists.")

    if User.one(Q.mobile == mobile):
        abort(400, description= f"Duplicate Entry, mobile - ({mobile}) already exists.")

    picture_cdn_url = None
    id_image_cdn_url = None

    if picture:
        picture_cdn_obj = uploader.upload(picture)
        picture_cdn_url = picture_cdn_obj['url']

    if id_image:
        id_image_cdn_obj = uploader.upload(id_image)
        id_image_cdn_url = id_image_cdn_obj['url']

    try:
        new_user = User(
        name=name,
        password=password,
        mobile=mobile,
        picture=picture_cdn_url,
        id_image=id_image_cdn_url,
        type=user_type)

        new_user.insert()
    except Exception as e:
        abort(400, description= f"There was an error while inserting new user, {e} .")

    # Convert Object to Dict
    new_user = new_user.to_json_type()

    access_token = create_access_token(identity={"name":new_user['name'], "id":new_user['_id']}, fresh=True)

    new_user['jwt_user'] = access_token

    # Remove Id and password from return obj
    new_user.pop('_id')
    new_user.pop('password')

    new_user['msg'] = 'Created successfully'
    new_user['status'] = 201

    return new_user


def update_user(request, current_user):
    # Check if user exists
    user = User.by_id(ObjectId(current_user['id']))
    if not user:
        abort(400, description=f"Not Found, ID - ({current_user['id']}) Dosen't Exist.")

    # Getting Values from form
    name = request.form.get('name')
    mobile = request.form.get('mobile')

    picture = request.files['picture']

    picture_filename = user.to_json_type()['picture']
    picture_cdn_url = None

    if picture:
        picture_cdn_obj = uploader.upload(picture)
        picture_cdn_url = picture_cdn_obj['url']

    try:
        new_user = User(
        _id=ObjectId(current_user['id']),
        name=name,
        mobile=mobile,
        picture=picture_cdn_url)

        new_user.update()
    except Exception as e:
        abort(400, description= f"There was an error while updating user, {e} .")

    return {'msg': 'Updated successfully', 'status': 201}


def delete_user(request):
    user = User.by_id(ObjectId(request['id']))

    if not user:
        abort(400, description=f"Not Found, ID - ({request['id']}) Dosen't Exist.")

    user.delete()

    return {'msg': 'Deleted successfully', 'status': 201}
