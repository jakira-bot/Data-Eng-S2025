import os
from google.cloud import pubsub_v1
from parse import Vehicle
import datetime

batch_settings = pubsub_v1.types.BatchSettings(
  max_bytes=1024 * 1024,
  max_latency=0.01,
  max_messages=1000,
)

publisher = pubsub_v1.PublisherClient(batch_settings=batch_settings)
project_id = "cloud-smedley-smedley"
topic_id = "tutorial"
topic_path = publisher.topic_path(project_id, topic_id)

def publish(msg):
    data = msg.encode("utf-8")
    future = publisher.publish(topic_path, data)

def send():
    time = datetime.datetime.now()
    print(f"Time A: {time}")
    count = 0
    test = Vehicle.from_json_bulk("bcsample.json")
    for msg in test:
        if(count % 10000 == 0):
            print(count)
        publish(repr(msg))
        count += 1
    publish(str(count))
    time = datetime.datetime.now()
    print(f"Time B: {time}")

def main():
    send()


if __name__ == "__main__":
    main()
    publisher.transport.close()