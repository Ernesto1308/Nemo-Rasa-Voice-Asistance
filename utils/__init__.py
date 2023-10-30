import base64
from datetime import timedelta, datetime

import requests
import json


# Serialize bytes to a string representation
def serialize_bytes(data: bytes) -> str:
    encoded_bytes = base64.b64encode(data).decode('utf-8')
    return encoded_bytes


# Deserialize string representation to bytes
def deserialize_bytes(encoded_bytes: str) -> bytes:
    decoded_bytes = base64.b64decode(encoded_bytes)
    return decoded_bytes


def set_rasa_verifier(user, medicine_name, medicine_hour):
    # Define the URL for the Rasa API
    url = f'http://localhost:5005/conversations/{user}/tracker/events?output_channel=callback&execute_side_effects=true'

    # Define the data to be sent to the Rasa API
    medicine_hour_str = datetime.isoformat(medicine_hour)
    reminder_time = datetime.isoformat(medicine_hour - timedelta(seconds=5))
    verifier_time = datetime.isoformat(medicine_hour + timedelta(seconds=5))
    entities = {"medicine": medicine_name, "medicine_hour": medicine_hour_str}

    data = [
        {
            "event": "reminder",
            "entities": entities,
            "intent": 'EXTERNAL_reminder',
            "date_time": reminder_time,
            "name": f'reminder {user}-{medicine_name}-{medicine_hour_str}',
            "kill_on_user_msg": False
        },
        {
            "event": "reminder",
            "entities": entities,
            "intent": 'EXTERNAL_verifier',
            "date_time": verifier_time,
            "name": f'verifier {user}-{medicine_name}-{medicine_hour_str}',
            "kill_on_user_msg": False
        }
    ]

    # Make a POST request to the Rasa API
    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    # Check if the request was successful
    if response.status_code == 200:
        print("Reminder successfully scheduled.")
    else:
        print("Error scheduling the reminder.")
