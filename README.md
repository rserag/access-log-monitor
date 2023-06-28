# Access Log Monitor

This Python script monitors the access.log file of an Nginx server and sends a message to a specified Telegram chat when a new log entry with a non-empty 'id' field is detected.

## Prerequisites

- Python 3.x
- `python-dotenv` library
- `requests` library
- `watchdog` library

## Installation

1. Clone the repository or download the script files.
2. Install the required Python libraries:
   ```shell
   pip install python-dotenv requests watchdog
3. Create a .env file in the project directory and define the following environment variables:
API_KEY: Your Telegram Bot API key.
CHAT_ID: The chat ID where you want to receive the messages.

## Usage

1. Modify the script as needed.
- Update the file path in the with open('/var/log/nginx/access.log') as f: line to point to your Nginx access log file.
- Customize the data extraction logic in the on_modified method based on the log format used in your access log file.
2. Run the script:
```shell
python access_log_monitor.py
```
3. The script will start monitoring the access log file for modifications. Whenever a new log entry with a non-empty 'id' field is detected, it will send a message to the specified Telegram chat using the Telegram Bot API.

## Notes
1. Ensure that the specified log file path is correct and accessible by the script.
2. Make sure to keep the .env file secure and exclude it from version control (e.g., by adding it to your .gitignore file) to protect sensitive information.
3. Customize the message format and API integration as per your requirements.
