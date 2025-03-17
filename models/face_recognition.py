from deepface import DeepFace
import os
import numpy as np
from models.database import FaceData, get_db

def recognize_face(image_path):
    try:
        # Get database session
        db = next(get_db())
        
        # Get all registered faces from database
        registered_faces = FaceData.get_all_faces(db)
        if not registered_faces:
            os.remove(image_path)
            return {"message": "No registered faces in database"}
        
        # Analyze input image
        input_result = DeepFace.analyze(img_path=image_path,
                                      actions=['emotion'],
                                      enforce_detection=False,
                                      detector_backend='opencv')
        
        if not input_result:
            os.remove(image_path)
            return {"message": "No face detected in input image"}
            
        if isinstance(input_result, list):
            input_result = input_result[0]
            
        # Compare with each registered face
        matches = []
        for face_data in registered_faces:
            try:
                verification = DeepFace.verify(img1_path=image_path,
                                            img2_path=face_data.face_path,
                                            enforce_detection=False,
                                            model_name="VGG-Face")
                
                if verification["verified"]:
                    matches.append({
                        "name": face_data.name,
                        "confidence": float(verification["distance"]),
                        "face_id": face_data.id
                    })
            except Exception as e:
                print(f"Error comparing with {face_data.name}: {str(e)}")
                continue
        
        # Remove input image
        os.remove(image_path)
        
        if matches:
            # Sort matches by confidence (lower distance means higher confidence)
            matches.sort(key=lambda x: x["confidence"])
            return {
                "faces_found": len(matches),
                "matches": matches
            }
        else:
            return {
                "faces_found": 0,
                "message": "No matching faces found",
                "matches": []
            }
            
    except Exception as e:
        if os.path.exists(image_path):
            os.remove(image_path)
        return {"error": str(e)}