# ~/app/api/status.py
from flask import jsonify
from app.api import bp


@bp.route('/test')
@bp.route('/')
def index():
    return jsonify({"status": 200, "message": "success", "data": {}}, 200)
