import os
from dotenv import load_dotenv

# Load environment variables from .env file in project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_root, '.env'))

class Config:
    # Require SECRET_KEY to be set - no insecure defaults
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///eastleigh_academy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'

    # Environment settings
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DOCKER_ENV = os.environ.get('DOCKER_ENV', 'false').lower() == 'true'