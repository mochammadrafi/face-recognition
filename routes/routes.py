from flask import Blueprint, request, jsonify
from controllers.home_controller import HomeController
from middlewares.auth_middleware import check_api_key
from controllers.face_controller import FaceController
from models.database import get_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return HomeController.index()

@main_bp.route('/api/face-detection', methods=['POST'])
def face_detection_route():
    check_api_key(request)
    return FaceController.face_detection(request)

@main_bp.route('/api/face-recognition', methods=['POST'])
def face_recognition_route():
    check_api_key(request)
    return FaceController.face_recognition(request)

@main_bp.route('/api/expression-detection', methods=['POST'])
def expression_detection_route():
    check_api_key(request)
    return FaceController.expression_detection(request)

# Endpoint baru untuk mengelola data wajah
@main_bp.route('/api/faces', methods=['POST'])
def register_face():
    check_api_key(request)
    return FaceController.register_face(request)

@main_bp.route('/api/faces', methods=['GET'])
def get_registered_faces():
    check_api_key(request)
    return FaceController.get_registered_faces(request)

@main_bp.route('/api/faces/<name>', methods=['GET'])
def get_face_by_name(name):
    check_api_key(request)
    return FaceController.get_face_by_name(request, name)