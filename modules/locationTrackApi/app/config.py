import os
from typing import List, Type

env = os.environ.get("ENV","test")

class BaseConfig:
    CONFIG_NAME = "base"    
    DEBUG = False    
    QUEUE_URL = os.environ.get("QUEUE_URL", "user1")
    QUEUE_TOPIC = os.environ.get("QUEUE_TOPIC", "user123")
    

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


EXPORT_CONFIGS = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]

config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
default_config = config_by_name[env]