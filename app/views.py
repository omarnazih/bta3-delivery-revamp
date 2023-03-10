from flask import jsonify, request, abort

from app import app
from app.util.util import get_current_timestamp, abort_missing_object_keys

from app.models import HelpRequests


@app.route('/')
def index():
    return {'msg':'Success', 'status': 200}


@app.route('/terms')
def terms():
    return jsonify({'msg':'Terms and conditions: all rights reserved to 3bdo 7naka', 'status': 201})


@app.post('/help')
def help():
    data = request.get_json()    
    abort_missing_object_keys(['message', 'name', 'phone'], data)
    
    try:
        help_obj = HelpRequests(message=data['message'], name=data['name'], phone=data['phone'], time_frame=get_current_timestamp())
        help_obj.insert()
    except Exception as e:
        abort(400, description=f"There was an error while inserting new request, {e}.")

    return jsonify({'msg':'Success', 'status': 201})


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def _handle_api_error(e):
    return jsonify({'msg': f'{e}', 'status': e.code})


@app.errorhandler(413)
def _handle_file_too_large(e):
    return jsonify({'msg': 'File is too large', 'status': e.code})