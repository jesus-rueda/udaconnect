import os
from typing import List, Type

env = os.environ.get("ENV","test")

DB_USERNAME = os.environ.get("DB_USERNAME", "user1")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "user123")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "locations")


class BaseConfig:
    CONFIG_NAME = "base"
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    QUEUE_URL = os.environ.get("QUEUE_URL", "user1")
    QUEUE_TOPIC = os.environ.get("QUEUE_TOPIC", "user123")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERSONS_API_URL = os.environ.get("PERSONS_API_URL", "http://localhost:5000/api")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "dev"   
    DEBUG = True    
    TESTING = False

class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"    
    DEBUG = True    
    TESTING = True   

class ProductionConfig(BaseConfig):
    CONFIG_NAME = "prod"    
    DEBUG = False    
    TESTING = False  


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]

config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
default_config = config_by_name[env]