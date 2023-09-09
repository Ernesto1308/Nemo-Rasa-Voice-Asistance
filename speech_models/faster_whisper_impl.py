import json

from faster_whisper import WhisperModel
from mqtt_provider import MqttSubscriber, MqttPublisher
from utils import write_audio, time
import base64


def on_message(client, userdata, message):
    print('Solicitud recibida', time())
    payload_decoded = eval(message.payload.decode('utf-8'))
    known_speaker = base64.b64decode(payload_decoded['audio'])
    write_audio(known_speaker, '../audios/speech_to_text.wav')
    segments, info = model.transcribe("../audios/speech_to_text.wav", beam_size=5)
    my_string = ''.join([segment.text for segment in segments])
    mqtt_publish = MqttPublisher('localhost', 'Speech Rec Module Output', 'audio/speech_rec_output')
    mqtt_publish.publish(
        value=json.dumps({
            "id_old_person": payload_decoded["id_old_person"],
            "old_person_name": payload_decoded["old_person_name"],
            "text": my_string,
        })
    )


model_size = "large-v2"
model = WhisperModel(model_size)
mqtt_subscribe = MqttSubscriber('localhost', 'Speech Rec Module Input', 'audio/speech_rec_input')
mqtt_subscribe.client.on_message = on_message
mqtt_subscribe.subscribe()
