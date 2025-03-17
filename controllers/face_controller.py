from flask import jsonify
import time
import os
import numpy as np
from deepface import DeepFace
from config.config import get_config
from models.expression_detection import detect_expression
from models.face_detection import detect_face
from models.face_recognition import recognize_face
from models.database import FaceData, get_db


class FaceController:
    @staticmethod
    def face_detection(request):
        try:
            if 'image' not in request.files:
                return jsonify({'error': 'No image provided'}), 400

            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f'uploaded-{timestamp}.jpg'
            file_path = os.path.join(get_config('UPLOAD_FOLDER'), filename)
            file.save(file_path)

            result = detect_face(file_path)
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def face_recognition(request):
        try:
            if 'image' not in request.files:
                return jsonify({'error': 'No image provided'}), 400

            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f'uploaded-{timestamp}.jpg'
            file_path = os.path.join(get_config('UPLOAD_FOLDER'), filename)
            file.save(file_path)

            result = recognize_face(file_path)
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def expression_detection(request):
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        file_path = os.path.join(get_config('UPLOAD_FOLDER'), file.filename)
        file.save(file_path)

        result = detect_expression(file_path)
        return jsonify({'result': result})

    @staticmethod
    def register_face(request):
        try:
            if 'image' not in request.files or 'name' not in request.form:
                return jsonify({'error': 'Image and name are required'}), 400

            file = request.files['image']
            name = request.form['name']

            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            # Simpan file
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f'{name}-{timestamp}.jpg'
            face_path = os.path.join('static/known_faces', filename)
            os.makedirs('static/known_faces', exist_ok=True)
            file.save(face_path)

            # Generate face encoding
            img_obj = DeepFace.analyze(img_path=face_path, 
                                     actions=['emotion'],
                                     enforce_detection=False)
            
            if not img_obj:
                os.remove(face_path)
                return jsonify({'error': 'No face detected in image'}), 400

            # Simpan ke database
            db = next(get_db())
            face_data = FaceData.create_face(
                db=db,
                name=name,
                face_path=face_path,
                face_encoding=str(img_obj)
            )

            return jsonify({
                'message': 'Face registered successfully',
                'face_id': face_data.id,
                'name': face_data.name
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_registered_faces(request):
        try:
            db = next(get_db())
            faces = FaceData.get_all_faces(db)
            return jsonify({
                'faces': [{
                    'id': face.id,
                    'name': face.name,
                    'face_path': face.face_path,
                    'created_at': face.created_at.isoformat()
                } for face in faces]
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_face_by_name(request, name):
        try:
            db = next(get_db())
            face = FaceData.get_face_by_name(db, name)
            if not face:
                return jsonify({'error': 'Face not found'}), 404

            return jsonify({
                'id': face.id,
                'name': face.name,
                'face_path': face.face_path,
                'created_at': face.created_at.isoformat()
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500