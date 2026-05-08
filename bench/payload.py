"""Mede o tamanho em bytes do payload de aplicação para gRPC e REST.

Compara apenas a camada de serialização (Protobuf vs JSON), sem contar
headers HTTP, frames HTTP/2, TCP, etc. É o número que entra no slide
'Tamanho do Payload'.

Pré-requisitos: gRPC server na :50051 e REST server na :8000.
"""

import grpc
import httpx

from grpc_server.generated import users_pb2, users_pb2_grpc

USER_ID = 1


def measure_grpc(user_id):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        request = users_pb2.UserRequest(id=user_id)
        response = stub.GetUser(request)
    return len(request.SerializeToString()), len(response.SerializeToString())


def measure_rest(user_id):
    with httpx.Client(base_url="http://localhost:8000") as client:
        response = client.get(f"/users/{user_id}")
    # GET nao tem body de request; so medimos a response
    return 0, len(response.content)


def main():
    grpc_req, grpc_resp = measure_grpc(USER_ID)
    rest_req, rest_resp = measure_rest(USER_ID)

    print(f"User id={USER_ID}\n")
    print(f"{'':<8} {'request':>10} {'response':>10}")
    print(f"{'gRPC':<8} {grpc_req:>10} {grpc_resp:>10}")
    print(f"{'REST':<8} {rest_req:>10} {rest_resp:>10}")
    print(f"\nResposta REST e {rest_resp / grpc_resp:.2f}x maior que gRPC.")


if __name__ == "__main__":
    main()
