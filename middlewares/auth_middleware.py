from flask import jsonify
import os

def check_api_key(request):
    API_KEY = os.getenv('API_KEY')
    api_key = request.headers.get('Authorization')
    if api_key != f"Bearer {API_KEY}":
        return jsonify({'error': 'Unauthorized'}), 401
    return None