import pulsar


def etl_ingest_consumer():
    client = pulsar.Client("pulsar://localhost:6650")
    # consumer = client.subscribe("persistent://sensor_mon/etl/ingest",
    #                             "sm_etl_ingest_subscription")
    consumer = client.subscribe("ingest", "ingest_subscription")

    while True:
        try:
            msg = consumer.receive()
            print("Received message '{}' id='{}'".format(msg.data(),
                                                         msg.message_id()))
            consumer.acknowledge(msg)
        except KeyboardInterrupt:
            client.close()
