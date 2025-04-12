from flask import Flask
from flask_cors import CORS

def create_app(config_name="development"):
    app = Flask(__name__)
    CORS(app)
    
    # Import and register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app