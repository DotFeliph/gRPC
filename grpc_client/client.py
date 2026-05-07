import grpc
import random
import time

from grpc_server.generated import users_pb2
from grpc_server.generated import users_pb2_grpc


channel = grpc.insecure_channel('localhost:50051')

stub = users_pb2_grpc.UserServiceStub(channel)

for i in range(10):
    print("--------------------------")
    print(f"teste {i}")
    TOTAL_REQUESTS = i*5000
    
    
    start = time.time()
    
    for _ in range(TOTAL_REQUESTS):
    
        user_id = random.choice([1, 2])
    
        response = stub.GetUser(
            users_pb2.UserRequest(id=user_id)
        )
    
    end = time.time()
    
    
    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Total time: {end - start:.2f} seconds")
    print(f"Requests/sec: {TOTAL_REQUESTS / (end - start):.2f}")
