def get_config(key, default=None):
    config = {
        "UPLOAD_FOLDER": "static/uploaded_images",
        "SECRET_KEY": "your_secret_key",
    }
    return config.get(key, default)