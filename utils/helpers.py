from os import environ
import requests
import json
from datetime import datetime

measurement_id = "G-G3V2DWQJQR"
api_secret = environ.get("GA_API_SECRET")
base_url = "https://www.google-analytics.com/mp/collect"
url = base_url + "?measurement_id=" + measurement_id + "&api_secret=" + api_secret
headers = {"Content-Type": "application/json"}


def log(message):
    """Prints a formatted log message"""
    print(f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] {message}')


def sendGaEvent(client_id, event_name, params={}):
    """Sends a POST request to the Google Analytics Measurement Protocol endpoint"""
    log(f'"DEBUG {api_secret} {client_id}')
    if client_id is None:
        log("client_id is not defined")
    else:
        r = requests.post(
            url,
            headers=headers,
            data=json.dumps(
                {
                    "client_id": client_id,
                    "events": [
                        {
                            "name": event_name,
                            "params": params,
                        }
                    ],
                }
            ),
        )
        log(f'"POST google-analytics.com" {r.status_code}')
