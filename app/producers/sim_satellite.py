import json
import random

from timeit import default_timer as dt

import pulsar

client = pulsar.Client("pulsar://localhost:6650")

# producer = client.create_producer("persistent://sensor_mon/etl/ingest")
producer = client.create_producer("ingest")

message_rate_min = 1
message_rate_max = 5

lat_min = 4500000
lat_max = 4900000

long_min = -12500000
long_max = -11700000

sat_names = [
    "sat0001",
    "sat0002",
    "sat0003",
    "sat0004",
    "sat0005",
    "sat0006",
    "sat0007",
]


def begin_search():
    # Simulate a notional set of satellites beaming down data on fireworks
    delay = random.randint(message_rate_min, message_rate_max)
    toc = dt()
    while True:
        try:
            if (dt() - toc) / delay > 1:
                message = {
                    "coords": [
                        random.randrange(lat_min, lat_max) / 100000.0,
                        random.randrange(long_min, long_max) / 100000.0
                    ],
                    "sat": random.choice(sat_names),
                    "data": {
                        "burst": round(random.normalvariate(10, 2), 4),
                        "intensity": round(random.normalvariate(5, 1), 4),
                        "fade": round(random.normalvariate(50, 8), 4),
                        "gradient": round(random.normalvariate(50, 10), 4),
                        "hue": round(random.normalvariate(50, 10), 4)
                    }
                }
                producer.send(bytes(json.dumps(message), 'utf8'))
                delay = random.randint(message_rate_min, message_rate_max)
                toc = dt()
        except KeyboardInterrupt:
            client.close()


if __name__ == "__main__":
    import threading

    threads = []
    for i in range(len(sat_names)):
        threads.append(threading.Thread(target=begin_search, daemon=False))
    for thread in threads:
        thread.start()
