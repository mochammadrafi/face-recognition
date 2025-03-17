from flask import jsonify

class HomeController:
    @staticmethod
    def index():
        # Return 404
        return jsonify({'error': 'Not found'}), 404