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
from flask_restx import Namespace, Resource, fields
from typing import Optional
import json
from app import app
import threading
from app.config import default_config

DATE_FORMAT = "%Y-%m-%d"


api = Namespace("connectionFinderApi", description="Connections via geolocation.")  # noqa

location = api.model("Location", {
    "id" : fields.Integer(description="The ID of the location"),    
    "longitude" : fields.String(description="The longitude of the location"),
    "latitude" : fields.String(description="The latitude of the location"),
    "person_id": fields.Integer(description="The ID of the person"),    
    "creation_time" : fields.DateTime(description="The creation date of the location in format YYYY-MM-DDTHH:MM:SS"),
})

person = api.model("Person", {
    "id" : fields.Integer(description="The ID of the person"),    
    "first_name" : fields.String(description="The first name of the person"),
    "last_name" : fields.String(description="The last name of the person"),
    "company_name": fields.String(description="The company of the person")
})  

connection = api.model("Connection", {
    "location" : fields.Nested(location),    
    "person" : fields.Nested(person)    
})

@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location")
class LocationResource(Resource):
   
    @responds(schema=LocationSchema)
    @api.doc(description="Retrieves the location by the given id")            
    @api.marshal_with(location, code=200, description='location')
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location


@api.route("/persons/<person_id>/connection")
@api.param("person_id", "Unique ID for a given Person")
class ConnectionDataResource(Resource):

    @api.doc(description="Retrieves the connections for a person based on a time range an a distance")            
    @api.param("start_date", "Lower bound of date range in format YYYY-MM-DD", _in="query")
    @api.param("end_date", "Upper bound of date range in format YYYY-MM-DD", _in="query")
    @api.param("distance", "Proximity to a given user in meters", _in="query")
    @api.marshal_with(connection, code=200, description='List of connections', as_list=True)
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

