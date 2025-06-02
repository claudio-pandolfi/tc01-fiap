from app.auth import register_auth
from app.config import Config
from app.routes import register_routes
from app.models import register_db_connection
from app.docs.schemas import get_schemas
from flasgger import Swagger
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config())

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "components": {
        "securitySchemes":{
            "BearerAuth": {
                "type": 'http',
                "scheme": 'bearer'
            }
        },
        "schemas" : get_schemas()
    },
    "security": {
        "BearerAuth": []
    },
    "specs_route": "/docs/"
}

swagger = Swagger(app, config=swagger_config)

register_auth(app)
register_db_connection(app)
register_routes(app)