import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from datetime import timedelta
import logging

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")  # e.g. mysql+pymysql://root:password@localhost:3306/newq
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default-secret-key")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)
    app.config["JWT_ALGORITHM"] = 'HS256'
    
    # Logging setup
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)

    # Initialize extensions
    jwt = JWTManager(app)
    from app.models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    from app.routes import api
    app.register_blueprint(api)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
