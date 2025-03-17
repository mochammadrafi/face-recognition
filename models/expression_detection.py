from deepface import DeepFace
import os

def detect_expression(image_path):
    try:
        # Analisis emosi menggunakan DeepFace
        result = DeepFace.analyze(image_path, 
                                actions=['emotion'],
                                enforce_detection=False)
        
        # Hapus file setelah diproses
        os.remove(image_path)
        
        if isinstance(result, list):
            result = result[0]
            
        emotions = result['emotion']
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])
        
        return {
            "dominant_emotion": dominant_emotion[0],
            "confidence": dominant_emotion[1],
            "all_emotions": emotions
        }
        
    except Exception as e:
        if os.path.exists(image_path):
            os.remove(image_path)
        return {"error": str(e)}