import grpc
import location_pb2_grpc
import location_pb2

message = location_pb2.LocationMessage()
message.person_id = 2
message.latitude = "4"
message.longitude = "72"
message.creation_time = "20220202T00:00:00"

channel = grpc.insecure_channel('192.168.50.4:30006')
stub = location_pb2_grpc.LocationServiceStub(channel)


stub.Register(message)
