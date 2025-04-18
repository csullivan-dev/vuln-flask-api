import os
from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest
from json import JSONDecodeError

from config import config
from app.extensions import db

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__, instance_relative_config=True)

    # Create instance directory if it doesn't exist
    os.makedirs(app.instance_path, exist_ok=True)

    # Load configuration from config dictionary
    app.config.from_object(config[config_name])

    # Override database URI only if not already specified in config
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(app.instance_path, 'sqlitedb.file')}"

    # Initialize extensions with the app
    db.init_app(app)

    # Enable CORS for all routes
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Register error handlers
    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return jsonify({"error": str(e)}), 400
    
    # Add specific handler for JSON decode errors
    @app.errorhandler(JSONDecodeError)
    def handle_json_error(e):
        return jsonify({"error": "Invalid JSON format"}), 400

    # Handle general request parse errors
    @app.before_request
    def handle_request_parsing():
        from flask import request
        if request.method in ["POST", "PUT", "PATCH"] and request.content_type == "application/json":
            # Force parsing of JSON so errors are caught early
            try:
                # This will raise JSONDecodeError for invalid JSON
                if request.data:
                    request.json
            except JSONDecodeError:
                return jsonify({"error": "Invalid JSON format"}), 400

    # Register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.blog_post_routes import blog_post_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(blog_post_bp)

    return app