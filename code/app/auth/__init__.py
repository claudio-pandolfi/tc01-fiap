from flask_jwt_extended import JWTManager

def register_auth(app):
    jwt = JWTManager(app)