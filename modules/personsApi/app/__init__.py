from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from app.init_db import init_db

db = SQLAlchemy()

def register_routes(api):
    from app.controllers import api as personsAPi
    api.add_namespace(personsAPi, path=f"/api")


def create_app(env=None):
    from app.config import config_by_name    

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="Persons API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api)
    db.init_app(app)    
    init_db()

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
