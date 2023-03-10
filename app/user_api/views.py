from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .controller import *

user_bp = Blueprint('user', __name__)

@user_bp.post('/signup')
def post_user():
    return create_user(request)


@user_bp.get('/')
@jwt_required()
def get_user():
    current_user = get_jwt_identity()    
    return jsonify(fetch_user(current_user))


@user_bp.put('/edit')
@jwt_required()
def put_user():
    current_user = get_jwt_identity()
    return update_user(request, current_user)


@user_bp.delete('/delete')
@jwt_required()
def del_user():
    current_user = get_jwt_identity()
    return delete_user(current_user) 


@user_bp.get('/all')
@jwt_required()
def get_users():
    return jsonify(fetch_all_users())
