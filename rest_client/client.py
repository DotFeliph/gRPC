import httpx
import random
import time


client = httpx.Client(base_url="http://localhost:8000")

for i in range(10):
    print("--------------------------")
    print(f"teste {i}")
    TOTAL_REQUESTS = i * 5000

    start = time.time()

    for _ in range(TOTAL_REQUESTS):

        user_id = random.choice([1, 2])

        response = client.get(f"/users/{user_id}")

    end = time.time()

    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Total time: {end - start:.2f} seconds")
    print(f"Requests/sec: {TOTAL_REQUESTS / (end - start):.2f}")
