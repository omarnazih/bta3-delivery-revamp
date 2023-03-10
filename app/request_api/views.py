from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .controller import *

req_bp = Blueprint('request', __name__)


@req_bp.post('/create')
@jwt_required()
def create_req():
    current_user = get_jwt_identity()
    return jsonify(create_request(request.json, current_user))


@req_bp.get('/get')
@jwt_required()
def get_req():
    current_user = get_jwt_identity()
    return jsonify(fetch_request(request.json, current_user))


@req_bp.get('/getall')
@jwt_required()
def get_all():
    current_user = get_jwt_identity()
    return jsonify(fetch_all_request(current_user))


@req_bp.get('/all')
@jwt_required()
def get_all_req():
    current_user = get_jwt_identity()
    return jsonify(fetch_all_req(current_user))


@req_bp.put('/update')
@jwt_required()
def update_req():
    current_user = get_jwt_identity()
    return jsonify(update_request(request.json, current_user))


@req_bp.delete('/delete')
@jwt_required()
def delete_req():
    return jsonify(delete_request(request.json))


@req_bp.put('/accept')
@jwt_required()
def accept_req():
    current_user = get_jwt_identity()
    status_changer = ReqStatus(request.json, current_user, RequestStatus.StatusAccept)
    return jsonify(status_changer.change_status())


@req_bp.put('/decline')
@jwt_required()
def decline_req():
    current_user = get_jwt_identity()
    status_changer = ReqStatus(request.json, current_user, RequestStatus.StatusDecline)
    return jsonify(status_changer.change_status())
