import grpc
import time
from datetime import datetime
from concurrent import futures
from app.location_pb2 import EmptyMessage
from app.location_pb2_grpc import LocationServiceServicer, add_LocationServiceServicer_to_server
from app.services import LocationService
from app.config import default_config

def print2(message):
  file_object = open('sample.txt', 'a')
  
  now = datetime.now()
  current_time = now.strftime("%m/%d/%Y - %H:%M:%S")

  # Append 'hello' at the end of file
  file_object.write(current_time + ":" + message)

  file_object.write('\n')

  # Close the file
  file_object.close()



class LocationServicer(LocationServiceServicer):

   def __init__(self):
        self._orders = []
        self.location_service = LocationService(default_config)

   def Register(self, request, context):
       print2("ENTRO")
       location = {
                "creation_time": request.creation_time,
                "latitude": request.latitude,
                "longitude": request.longitude,
                "person_id": request.person_id
        }

       self.location_service.create(location)       
       return EmptyMessage()

   
print2("SERVER INIT")
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))        
add_LocationServiceServicer_to_server(LocationServicer(), server)


server.add_insecure_port("[::]:5001")
server.start()
print2("SERVER STARTED")
try:
    while True:
         time.sleep(86400)
except:
    print2("ERROR")
    server.stop(0)