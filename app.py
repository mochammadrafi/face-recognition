from flask import Flask
from dotenv import load_dotenv
from routes.routes import main_bp

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploaded_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)