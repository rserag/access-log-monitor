import time
from dotenv import dotenv_values
from user_agents import parse
from ipwhois import IPWhois
from requests import get
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

config = dotenv_values(".env")

api_key = config["API_KEY"]
chat_id = config["CHAT_ID"]

# Utility function to get nested values from dictionaries
def get_value(data, key):
    keys = key.split('.')
    value = data
    for k in keys:
        value = value.get(k)
        if value is None:
            break
    return value

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
            whois = IPWhois(data['rem_add'])
            result = whois.lookup_rdap()
            keys = ['asn', 'asn_country_code', 'network.name', 'asn_description']

            # parse the user-agent and add into dict
            ua = str(parse(data['usr']))            
            del data['usr']
            data['UA'] = ua

            # remove X-Forwarded-For if redundant
            if data['rem_add'] == data['x_fwd']:
                del data['x_fwd']

            # remove empty key/value pair such as referrer
            pruned_data = {k: v for k, v in data.items() if v}

            # stringify the data from the request itself
            initial_data = "\n".join([f"{key} = {value}" for key, value in pruned_data.items()])

            # add the whois info
            message = initial_data + "\n" + "\n".join([f"{key}: {get_value(result, key)}" for key in keys])

            # send the data the to the bot
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
