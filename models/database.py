from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

# Buat koneksi database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///face_recognition.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class FaceData(Base):
    __tablename__ = "face_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    face_path = Column(String)  # Path ke file wajah
    face_encoding = Column(String)  # Encoding wajah dalam format string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    @classmethod
    def create_face(cls, db, name, face_path, face_encoding):
        face_data = cls(
            name=name,
            face_path=face_path,
            face_encoding=face_encoding
        )
        db.add(face_data)
        db.commit()
        db.refresh(face_data)
        return face_data

    @classmethod
    def get_all_faces(cls, db):
        return db.query(cls).all()

    @classmethod
    def get_face_by_name(cls, db, name):
        return db.query(cls).filter(cls.name == name).first()

# Buat tabel
Base.metadata.create_all(bind=engine)

# Fungsi untuk mendapatkan DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 