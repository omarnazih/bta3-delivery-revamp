from flask import abort, session
from mongoframes import *
from bson.objectid import ObjectId

from flask_jwt_extended import create_access_token

from app.util.util import abort_missing_object_key
from app.util.util import abort_missing_object_keys

from app.models import User
from app.user_api.controller import fetch_user


def login(request):
  abort_missing_object_keys(['mobile', 'password'], request)

  user = User.one(And(Q.mobile==request['mobile'], Q.password==request['password']), projection={'id': {"$toString": "$_id"}, '_id':0})

  if not user:
    abort(400, description="Not Found, No users Found with this credentials.")

  return fetch_user(user)


def confirm_number(request):
  abort_missing_object_key('mobile', request)

  user = User.one(Q.mobile == request['mobile'], projection={"$toString": "$_id"})

  if not user:    
    abort(400, description=f"Not Found, this number - '{request['mobile']}' is not linked to any user.")

  return {'msg': 'User is found', 'status': 201}


def reset_password(request):
  abort_missing_object_keys(['mobile', 'password'], request)

  user = User.one(Q.mobile == request['mobile'])

  if not user:
    abort(400, description=f"Not Found, this number - '{request['mobile']}' is not linked to any user.")
  
  try:
    user.password = request['password']
    user.update()
  except Exception as e:
    abort(400, description= f"There was an error while updating user, {e}.")    

  return {'msg': 'Updated successfully', 'status': 201}

