from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from kafka import KafkaConsumer
from flask_sqlalchemy import SQLAlchemy
from app.init_db import init_db

db = SQLAlchemy()
app = Flask(__name__)

def register_routes(api, app, root="api"):
    from app.controllers import api as connectionsApi
    api.add_namespace(connectionsApi, path=f"/api")

def create_app(env=None):
    from app.config import config_by_name    
    
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="Connection Finder API", version="0.1.0")
    
    CORS(app)  # Set CORS for development
    
    db.init_app(app)
    register_routes(api, app)   
    init_db()

    
    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
