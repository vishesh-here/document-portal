import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-123')
    DOCUMENT_PASSWORD = os.environ.get('DOCUMENT_PASSWORD', '1234')
    
    # Database
    def get_db_path(self):
        if os.environ.get('RENDER'):
            # Use the directory that Render.com provides for persistent storage
            return os.path.join(os.environ.get('RENDER_VOLUME_PATH', '/tmp'), 'documents.db')
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'documents.db')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# User credentials - In production, these should be stored securely
USER_CREDENTIALS = {
    'user@example.com': 'password123',
    'admin@example.com': 'admin123'
}