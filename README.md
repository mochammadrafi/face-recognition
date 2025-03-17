# Face Recognition API

Sistem Face Recognition API dengan fitur deteksi wajah, pengenalan wajah, dan deteksi ekspresi menggunakan DeepFace.

## Fitur

- 👤 Deteksi Wajah
- 🎭 Deteksi Ekspresi
- 🔍 Pengenalan Wajah
- 💾 Database Integration
- 🔐 API Key Authentication

## Teknologi

- Python 3.8+
- Flask
- DeepFace
- SQLAlchemy
- OpenCV

## Instalasi

1. Clone repository:
```bash
git clone [url-repository]
cd face-recognition
```

2. Buat virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup environment variables:
```bash
cp .env.example .env
# Edit .env dan isi API_KEY
```

5. Buat folder yang diperlukan:
```bash
mkdir -p static/known_faces
mkdir -p static/detected_faces
mkdir -p static/uploaded_images
mkdir -p static/fail_image
```

## Penggunaan

1. Jalankan aplikasi:
```bash
python app.py
```

2. API Endpoints:

### Deteksi Wajah
```bash
POST /api/face-detection
Header: Authorization: Bearer YOUR_API_KEY
Body: form-data
- image: [file gambar]
```

### Pengenalan Wajah
```bash
POST /api/face-recognition
Header: Authorization: Bearer YOUR_API_KEY
Body: form-data
- image: [file gambar]
```

### Deteksi Ekspresi
```bash
POST /api/expression-detection
Header: Authorization: Bearer YOUR_API_KEY
Body: form-data
- image: [file gambar]
```

### Registrasi Wajah
```bash
POST /api/faces
Header: Authorization: Bearer YOUR_API_KEY
Body: form-data
- image: [file gambar]
- name: "nama_orang"
```

### Lihat Wajah Terdaftar
```bash
GET /api/faces
Header: Authorization: Bearer YOUR_API_KEY
```

### Cari Wajah berdasarkan Nama
```bash
GET /api/faces/{nama}
Header: Authorization: Bearer YOUR_API_KEY
```

## Struktur Folder

```
project_root/
├── models/
│   ├── database.py
│   ├── face_detection.py
│   ├── face_recognition.py
│   └── expression_detection.py
├── controllers/
│   ├── face_controller.py
│   └── home_controller.py
├── routes/
│   └── routes.py
├── static/
│   ├── known_faces/      # Wajah terdaftar
│   ├── detected_faces/   # Hasil deteksi
│   ├── uploaded_images/  # Upload temporary
│   └── fail_image/      # Gambar gagal
├── instance/
│   └── face_recognition.db
├── .env
├── app.py
└── requirements.txt
```

## Response Format

### Successful Face Recognition
```json
{
    "faces_found": 1,
    "matches": [
        {
            "name": "john_doe",
            "confidence": 0.89,
            "face_id": 1
        }
    ]
}
```

### Error Response
```json
{
    "error": "Error message"
}
```

## Kontribusi

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## Lisensi

Distributed under the MIT License. See `LICENSE` for more information.