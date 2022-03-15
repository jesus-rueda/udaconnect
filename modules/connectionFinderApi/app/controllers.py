from datetime import datetime

from app.models import  Location
from app.schemas import (
    ConnectionSchema,
    LocationSchema,    
)
from kafka import KafkaConsumer
from app.services import ConnectionService, LocationService
from flask import request
from flask_accepts import responds
from flask_restx import Namespace, Resource
from typing import Optional
import json
from app import app
import threading
from app.config import default_config

DATE_FORMAT = "%Y-%m-%d"


api = Namespace("connectionFinderApi", description="Connections via geolocation.")  # noqa

@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
   
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)
        
        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results

def read_locations():    
    with app.app_context():
        consumer = KafkaConsumer(default_config.QUEUE_TOPIC, bootstrap_servers=default_config.QUEUE_URL,  value_deserializer=lambda m: json.loads(m.decode('utf-8')),)
        for message in consumer:
            location_json = message.value
            location = LocationService.create(location_json)
            print(location)

t = threading.Thread(target=read_locations, daemon=True)
t.start()

