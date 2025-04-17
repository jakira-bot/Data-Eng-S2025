import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import json
import datetime

def fetch():
    project_id = "cloud-smedley-smedley"
    subscription_id = "tutorial-sub"
    timeout = 135.0

    messages = []

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    time = datetime.datetime.now()
    print(f"Time A: {time}")

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        nonlocal time
        messages.append(message.data.decode('utf-8'))
        time = datetime.datetime.now()
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()

    
    print(f"Done")
    print(f"Time B: {time}")
    print("Pulled msgs: " + str(len(messages)))

def main():
    fetch()


if __name__ == "__main__":
    main()