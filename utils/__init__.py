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


def write_audio(data_bytes, audio):
    with open(audio, mode='wb') as aud:
        aud.write(data_bytes)
        aud.close()


def read_audio(audio):
    with open(audio, mode='rb') as text_speech:
        data_bytes = text_speech.read()
        text_speech.close()

    return data_bytes


def time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


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


numbers = {
    1: 'uno', 2: 'dos', 3: 'tres', 4: 'cuatro', 5: 'cinco',
    6: 'seis', 7: 'siete', 8: 'ocho', 9: 'nueve', 10: 'diez',
    11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce', 15: 'quince',
    16: 'dieciséis', 17: 'diecisiete', 18: 'dieciocho', 19: 'diecinueve',
    20: 'veinte', 21: 'veintiuno', 22: 'veintidós', 23: 'veintitrés',
    24: 'veinticuatro', 25: 'veinticinco', 26: 'veintiséis', 27: 'veintisiete',
    28: 'veintiocho', 29: 'veintinueve', 30: 'treinta', 31: 'treinta y uno',
    32: 'treinta y dos', 33: 'treinta y tres', 34: 'treinta y cuatro',
    35: 'treinta y cinco', 36: 'treinta y seis', 37: 'treinta y siete',
    38: 'treinta y ocho', 39: 'treinta y nueve', 40: 'cuarenta',
    41: 'cuarenta y uno', 42: 'cuarenta y dos', 43: 'cuarenta y tres',
    44: 'cuarenta y cuatro', 45: 'cuarenta y cinco', 46: 'cuarenta y seis',
    47: 'cuarenta y siete', 48: 'cuarenta y ocho', 49: 'cuarenta y nueve',
    50: 'cincuenta', 51: 'cincuenta y uno', 52: 'cincuenta y dos',
    53: 'cincuenta y tres', 54: 'cincuenta y cuatro', 55: 'cincuenta y cinco',
    56: 'cincuenta y seis', 57: 'cincuenta y siete', 58: 'cincuenta y ocho',
    59: 'cincuenta y nueve'
}
