import time
from dotenv import dotenv_values
from requests import get
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

config = dotenv_values(".env")

api_key = config["API_KEY"]
chat_id = config["CHAT_ID"]

class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # get the last line from the logs
        with open('/var/log/nginx/access.log') as f:
            for line in f:
                pass
            last_line = line

        # extract the data fields by delimiter
        parts = last_line.split('***')
        parts = parts[1:-1]
        data = {}

        # ingest the data into a dictionary
        for part in parts:
            try:
                key, value = part.split('=')
                data[key] = value
            except ValueError:
                pass

        # check whether the ID is empty
        if data['id']:
            message = "\n".join([f"{key} = {value}" for key, value in data.items()])
            url = f'https://api.telegram.org/bot{api_key}/sendMessage?chat_id={chat_id}&text={message}'
            get(url).json()
        else:
            pass

event_handler = FileModifiedHandler()
observer = Observer()
observer.schedule(event_handler, path='/var/log/nginx', recursive=False)

observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt: 
    observer.stop()
observer.join()
