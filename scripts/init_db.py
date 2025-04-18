#!/usr/bin/env python3
import os
import sys
from app import create_app
from app.extensions import db

def init_database():
    config_name = os.environ.get('FLASK_CONFIG', 'default')
    app = create_app(config_name)
    
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
            return True
        except Exception as e:
            print(f"Database initialization failed: {e}", file=sys.stderr)
            return False

# Add this to make the script runnable directly
if __name__ == "__main__":
    success = init_database()
    if not success:
        sys.exit(1)