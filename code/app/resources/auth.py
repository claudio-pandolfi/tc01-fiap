from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from flasgger import swag_from

class Auth(Resource):
    @swag_from('../docs/auth/auth.yml', methods=["GET"])
    def get(self):
        username = request.args.get("username")
        password = request.args.get("password")
        if username != "test" or password != "test":
            return { 'status': 401, 'message' : 'Usuário ou senha inválida'}, 401

        access_token = create_access_token(identity=username)
        return { 'status': 200, 'access_token' : access_token}, 200

class Home(Resource):
    def get(self):
        return {'message': 'Welcome'}