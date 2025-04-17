# Made to upload 100 buses from a folder, folder is not pushed to github

import os
from google.cloud import pubsub_v1
from parse import Vehicle
import datetime
from datetime import date

def list_files_in_directory(folder_path):
  try:
    files = os.listdir(folder_path)
    return [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
  except FileNotFoundError:
    return f"Error: Folder '{folder_path}' not found."
  except NotADirectoryError:
    return f"Error: '{folder_path}' is not a directory."

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
    atime = datetime.datetime.now()
    print(f"Time A: {atime}")
    today = date.today()
    new_folder_path = "./2025-04-16"
    files = list_files_in_directory(new_folder_path)
    count = 0
    for id in files:
        test = Vehicle.from_json_bulk("2025-04-16/" + id)
        for msg in test:
            if(count % 10000 == 0):
                print(count)
            publish(repr(msg))
            count += 1
    publish(str(count))
    print(f"Time A: {atime}")
    time = datetime.datetime.now()
    print(f"Time B: {time}")

def main():
    send()


if __name__ == "__main__":
    main()
    publisher.transport.close()