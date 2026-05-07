from grpc_tools import protoc

protoc.main([
    '',
    '-I./proto',
    '--python_out=./grpc_server/generated',
    '--grpc_python_out=./grpc_server/generated',
    './proto/users.proto'
])
