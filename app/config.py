import os

class Config:
    FLASK_APP='run.py'
    DEBUG = False
    UPLOAD_DIR = os.environ.get('UPLOAD_DIR', '/output')

class DevelopmentConfig(Config):
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', True)
    MAX_CONTENT_LENGTH = 10 * 1024 # 10 KB

class ProductionConfig(Config):
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
    MAX_CONTENT_LENGTH = int(os.environ.get(
        'MAX_CONTENT_LENGTH', 
        10 * 1024 * 1024 # 10 MB
    ))

# You can add more configuration classes for different environments if needed

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    # Add more environments if needed
}