import logging
from typing import Dict
from kafka import KafkaProducer
import json


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("locationTrack-api")

class LocationService:         
    
    def __init__(self, config):
        self.server = config.QUEUE_URL
        self.topic_name = config.QUEUE_TOPIC
        self.producer = KafkaProducer(bootstrap_servers=self.server)
        

    def create(self, location: Dict) -> None:             
        print(location)
        data = bytearray(json.dumps(location), "UTF-8")

        self.producer.send(self.topic_name, data)
        self.producer.flush()

        

