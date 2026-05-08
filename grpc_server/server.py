from concurrent import futures
import grpc
import time
import random

from grpc_server.generated import users_pb2
from grpc_server.generated import users_pb2_grpc

users_db = {
    1: {
        "id": 1,
        "name": "Antonio Marques",
        "email": "antonio@email.com",
        "phone": "+55 21 99999-9999",
        "address": "Rua Exemplo 123",
        "city": "Rio de Janeiro",
        "state": "RJ",
        "country": "Brazil",
        "zipcode": "20000-000",
        "company": "Open Systems",
        "job_title": "Software Engineer",
        "biography": "A" * 300,
        "preferences": "dark_mode=true;notifications=true;" * 5,
        "metadata": "metadata_example_" * 5,
        "notes": "important_notes_" * 5,
        "age": 28,
        "followers_count": 1247,
        "following_count": 389,
        "posts_count": 2341,
        "reputation_score": 4.7,
        "is_active": True,
        "is_verified": False,
        "is_premium": True,
        "created_at": 1714000000,
        "updated_at": 1714500000,
    },

    2: {
        "id": 2,
        "name": "Maria Silva",
        "email": "maria@email.com",
        "phone": "+55 11 98888-8888",
        "address": "Avenida Central 456",
        "city": "São Paulo",
        "state": "SP",
        "country": "Brazil",
        "zipcode": "01000-000",
        "company": "Tech Corp",
        "job_title": "Data Analyst",
        "biography": "B" * 300,
        "preferences": "light_mode=false;notifications=false;" * 5,
        "metadata": "other_metadata_" * 5,
        "notes": "secondary_notes_" * 5,
        "age": 35,
        "followers_count": 8523,
        "following_count": 142,
        "posts_count": 891,
        "reputation_score": 4.9,
        "is_active": True,
        "is_verified": True,
        "is_premium": False,
        "created_at": 1700000000,
        "updated_at": 1714600000,
    }
}


class UserService(users_pb2_grpc.UserServiceServicer):

    def GetUser(self, request, context):

        user = users_db.get(request.id)

        return users_pb2.UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            phone=user["phone"],
            address=user["address"],
            city=user["city"],
            state=user["state"],
            country=user["country"],
            zipcode=user["zipcode"],
            company=user["company"],
            job_title=user["job_title"],
            biography=user["biography"],
            preferences=user["preferences"],
            metadata=user["metadata"],
            notes=user["notes"],
            age=user["age"],
            followers_count=user["followers_count"],
            following_count=user["following_count"],
            posts_count=user["posts_count"],
            reputation_score=user["reputation_score"],
            is_active=user["is_active"],
            is_verified=user["is_verified"],
            is_premium=user["is_premium"],
            created_at=user["created_at"],
            updated_at=user["updated_at"],
        )

    def UpdateUser(self, request, context):

        if request.id in users_db:
            users_db[request.id]["biography"] = request.biography
            return users_pb2.UpdateResponse(success=True)

        return users_pb2.UpdateResponse(success=False)


def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    users_pb2_grpc.add_UserServiceServicer_to_server(
        UserService(),
        server
    )

    server.add_insecure_port('[::]:50051')

    server.start()

    print("gRPC Server running on port 50051")

    server.wait_for_termination()


if __name__ == '__main__':
    serve()
