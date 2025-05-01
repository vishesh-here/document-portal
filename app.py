from flask import Flask
from models import init_db
from routes import init_routes
from config import DevelopmentConfig, ProductionConfig
import os

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the database
    with app.app_context():
        init_db()

    # Register routes
    init_routes(app)

    return app

if __name__ == '__main__':
    app = create_app(ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else DevelopmentConfig)
    app.run()