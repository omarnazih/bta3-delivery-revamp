from flask import Blueprint, request, jsonify

from .controller import *

auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/login')
def auth_login():
    return jsonify(login(request.json))


@auth_bp.post('/signup')
def auth_signup():
    return {'msg': 'api replaced with `user/signup`', 'status': 400}


@auth_bp.post('/confirm-mobile')
def auth_confirm_mobile():
    return jsonify(confirm_number(request.json))


@auth_bp.put('/reset-password')
def auth_reset_password():
    return jsonify(reset_password(request.json))
