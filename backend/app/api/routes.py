from app.api import api_bp
from flask import jsonify

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "API is operational"})