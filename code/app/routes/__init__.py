from flask_restful import Api
from app.resources.auth import Auth, Home
from app.routes.exportation import exportation_routes
from app.routes.importation import importation_routes
from app.routes.processing import processing_routes
from app.routes.production import production_routes
from app.routes.trading import trading_routes

def register_routes(app):
    api = Api(app)
    
    api.add_resource(Auth, '/auth')
    api.add_resource(Home, '/')
    exportation_routes(api)
    importation_routes(api)
    processing_routes(api)
    production_routes(api)
    trading_routes(api)
