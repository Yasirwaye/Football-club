import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
# (in production/Railway, variables come from environment directly)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(project_root, '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)

class Config:
    # SECRET_KEY - use environment variable or fallback for development
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///eastleigh_academy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'

    # Environment settings
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DOCKER_ENV = os.environ.get('DOCKER_ENV', 'false').lower() == 'true'