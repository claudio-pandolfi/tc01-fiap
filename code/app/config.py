import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.root_path = '/code'
        self.SWAGGER = {
            'title': os.getenv('SWAGGER_TITLE'),
            'uiversion': int(os.getenv('SWAGGER_UI_VERSION', 3)),
            'version': os.getenv('API_VERSION'),
            'description': os.getenv('API_DESCRIPTION'),
            'openapi' : '3.0.2'
        }
        self.MONGODB_URL = os.getenv('MONGODB_URL')
        self.DEBUG = os.getenv('FLASK_DEBUG')
        self.FLASK_ENV = os.getenv('FLASK_ENV')
        self.JWT_SECRET_KEY = os.getenv('SECRET_KEY')
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
        self.MONGODB_HOST = os.getenv('MONGODB_HOST')
        self.MONGODB_PORT = int(os.getenv('MONGODB_PORT'))
        self.REDIS_URL = os.getenv('REDIS_URL')
        self.EMBRAPA_URL = os.getenv('EMBRAPA_URL')