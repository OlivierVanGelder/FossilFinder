from flask import Flask
from config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.chat import chat_bp  # <-- Add this

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)      # <-- And this

    return app
