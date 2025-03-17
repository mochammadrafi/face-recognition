from deepface import DeepFace
import cv2
import os
import time

def detect_face(image_path):
    try:
        # Deteksi wajah menggunakan DeepFace.analyze
        result = DeepFace.analyze(img_path=image_path, 
                                actions=['emotion'],
                                enforce_detection=False,
                                detector_backend='opencv')
        
        # Baca gambar untuk visualisasi
        img = cv2.imread(image_path)
        
        if result:
            results = result if isinstance(result, list) else [result]
            
            # Buat folder untuk menyimpan wajah yang terdeteksi
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            faces_folder = f'static/detected_faces/faces_{timestamp}'
            os.makedirs(faces_folder, exist_ok=True)
            
            # Untuk setiap wajah yang terdeteksi
            face_files = []
            for idx, face_data in enumerate(results):
                if 'region' in face_data:
                    region = face_data['region']
                    x = region['x']
                    y = region['y']
                    w = region['w']
                    h = region['h']
                    
                    # Tambahkan padding 20% untuk setiap sisi
                    padding_x = int(w * 0.2)
                    padding_y = int(h * 0.2)
                    
                    # Sesuaikan koordinat dengan padding
                    start_x = max(0, x - padding_x)
                    start_y = max(0, y - padding_y)
                    end_x = min(img.shape[1], x + w + padding_x)
                    end_y = min(img.shape[0], y + h + padding_y)
                    
                    # Crop wajah
                    face_crop = img[start_y:end_y, start_x:end_x]
                    
                    # Simpan wajah yang di-crop
                    face_file = f'{faces_folder}/face_{idx+1}.jpg'
                    cv2.imwrite(face_file, face_crop)
                    face_files.append(face_file)
                    
                    # Gambar rectangle di gambar original
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            if face_files:
                # Simpan gambar dengan semua rectangle
                full_image_path = f'{faces_folder}/full_detected.jpg'
                cv2.imwrite(full_image_path, img)
                
                # Hapus file original
                os.remove(image_path)
                return True
        
        # Jika tidak ada wajah terdeteksi
        os.makedirs('static/fail_image', exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        fail_path = f'static/fail_image/fail-{timestamp}.jpg'
        cv2.imwrite(fail_path, img)
        os.remove(image_path)
        return False
        
    except Exception as e:
        print(f"Error in face detection: {str(e)}")
        os.makedirs('static/fail_image', exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        fail_path = f'static/fail_image/fail-{timestamp}.jpg'
        
        img = cv2.imread(image_path)
        if img is not None:
            cv2.imwrite(fail_path, img)
            
        if os.path.exists(image_path):
            os.remove(image_path)
        return False