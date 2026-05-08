import argparse
import csv
import random
import time
from pathlib import Path

CSV_PATH = Path("bench/results.csv")
CSV_HEADER = [
    "protocol",
    "latency_ms",
    "run",
    "total_requests",
    "total_time",
    "requests_per_sec",
]


def make_grpc_caller():
    import grpc
    from grpc_server.generated import users_pb2, users_pb2_grpc

    channel = grpc.insecure_channel("localhost:50051")
    stub = users_pb2_grpc.UserServiceStub(channel)

    def call(user_id):
        stub.GetUser(users_pb2.UserRequest(id=user_id))

    return call


def make_rest_caller():
    import httpx

    client = httpx.Client(base_url="http://localhost:8000")

    def call(user_id):
        client.get(f"/users/{user_id}")

    return call


def run_benchmark(call, total_requests):
    # warmup: descarta a primeira request pra nao medir TCP handshake / cache miss
    call(1)

    start = time.time()
    for _ in range(total_requests):
        user_id = random.choice([1, 2])
        call(user_id)
    elapsed = time.time() - start

    rps = total_requests / elapsed if elapsed > 0 else 0.0
    return elapsed, rps


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("protocol", choices=["grpc", "rest"])
    parser.add_argument("--total-requests", type=int, default=10000)
    parser.add_argument(
        "--latency-ms",
        type=int,
        default=0,
        help="Apenas tag pra registrar no CSV. A latência real é configurada com 'tc' externamente.",
    )
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()

    caller = make_grpc_caller() if args.protocol == "grpc" else make_rest_caller()

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    is_new = not CSV_PATH.exists()

    with open(CSV_PATH, "a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(CSV_HEADER)

        for run in range(1, args.repeats + 1):
            print(
                f"[{args.protocol}] run {run}/{args.repeats}: "
                f"{args.total_requests} reqs @ {args.latency_ms}ms latency"
            )
            elapsed, rps = run_benchmark(caller, args.total_requests)
            w.writerow(
                [
                    args.protocol,
                    args.latency_ms,
                    run,
                    args.total_requests,
                    f"{elapsed:.4f}",
                    f"{rps:.2f}",
                ]
            )
            f.flush()
            print(f"  {elapsed:.2f}s -> {rps:.2f} req/s")


if __name__ == "__main__":
    main()
