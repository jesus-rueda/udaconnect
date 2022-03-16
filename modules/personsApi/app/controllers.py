from http.client import responses
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource, fields

from app.models import Person
from app.schemas import (    
    PersonSchema,
)
from app.services import PersonService
from typing import List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("PersonsApi", description="Persons registry service, provide creation and query of persons data")  # noqa

person_fields = {
    "id" : fields.Integer(description="The ID of the person"),    
    "first_name" : fields.String(description="The first name of the person"),
    "last_name" : fields.String(description="The last name of the person"),
    "company_name": fields.String(description="The company of the person")
}

person_req_fields = dict(person_fields)
del person_req_fields["id"]

person_request = api.model("PersonRequest", person_req_fields)
person = api.model("Person", person_fields)

@api.route("/persons")
class PersonsResource(Resource):

    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    @api.doc(description="Creates a new person in registry")
    @api.expect(person_request)
    @api.marshal_with(person, code=200, description='Person created')
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    @api.doc(description="Retrieves the list of persons")            
    @api.marshal_with(person, code=200, description='List of persons', as_list=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons

@api.route("/persons/by-ids")
class PersonsQueryResource(Resource):    
    @responds(schema=PersonSchema, many=True)
    @api.doc(description="Retrieves the persons by the given ids")        
    @api.param('ids', 'Comma separated list of person IDs', _in="query")
    @api.marshal_with(person, code=200, description='List of persons', as_list=True)
    def get(self) -> List[Person]:
        ids = [int(id) for id in request.args["ids"].split(",")]
        persons: List[Person] = PersonService.retrieve_multiple(ids)
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    @api.doc(description="Retrieves the person by the given id")            
    @api.marshal_with(person, code=200, description='The person')
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person

