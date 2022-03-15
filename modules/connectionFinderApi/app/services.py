import logging
from datetime import datetime, timedelta
from typing import Dict, List
from app.config import default_config
from geoalchemy2.functions import ST_Point
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text


from app import db
from app.models import Connection, Location
from app.schemas import LocationSchema

import requests

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")


class ConnectionService:
    
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        persons_ids = []      

        # Prepare arguments for queries
        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[Connection] = []
        for line in tuple(data):
            for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
            ) in db.engine.execute(query, **line):
                location = Location(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=exposed_time,
                )
                location.set_wkt_with_coords(exposed_lat, exposed_long)
                persons_ids.append(exposed_person_id)
                result.append(
                    Connection(
                        person=exposed_person_id, location=location,
                    )
                )

        # call the persons api        
        
        if len(persons_ids) > 0:
            persons_api_url = default_config.PERSONS_API_URL
            persons_response = requests.get(persons_api_url + "/persons/by-ids?ids="+",".join([str(id) for id in persons_ids]))         
            persons = {person["id"]:person for person in persons_response.json()}        
            
        for connection in result:
            person_id = connection.person
            connection.person = persons[person_id]
        
        return result


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.set_wkt_with_coords(location["latitude"], location["longitude"])
        db_shape = new_location.wkt_shape.replace("ST_POINT", "POINT")
        
        import psycopg2
        conn = psycopg2.connect(default_config.SQLALCHEMY_DATABASE_URI)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO location (person_id, creation_time, coordinate) VALUES (%(person_id)s, %(creation_time)s, %(coordinate)s)
        """, {"person_id": new_location.person_id, "creation_time":new_location.creation_time, "coordinate": db_shape})

        #db.session.add(new_location)        
        #db.session.commit()

        return new_location
