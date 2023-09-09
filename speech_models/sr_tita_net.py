import nemo.collections.asr as nemo_asr
import json
import base64
from speech_models.mqtt_provider import MqttSubscriber, MqttPublisher
from utils import write_audio, time
from acces_data_layer.services import old_person_service


def on_message(client, userdata, message):
    print('Solicitud recibida', time())
    payload_decoded = eval(message.payload.decode('utf-8'))
    unknown_speaker_bytes = bytes(payload_decoded['unknown_speaker'])
    write_audio(unknown_speaker_bytes, '../audios/unknown_speaker.wav')
    authenticated_op = None
    old_person_list = old_person_service.select()

    for current_old_person in old_person_list:
        write_audio(current_old_person.audio, '../audios/known_speaker.wav')

        if speaker_model.verify_speakers('../audios/known_speaker.wav', '../audios/unknown_speaker.wav'):
            authenticated_op = current_old_person
            break

    mqtt_publisher = MqttPublisher('localhost', 'Verification Module Output', 'audio/verification_output')

    if authenticated_op:
        authenticated_op = authenticated_op.to_dict()
        unknown_speaker_string = base64.b64encode(unknown_speaker_bytes).decode('utf-8')
        authenticated_op['audio'] = unknown_speaker_string
        mqtt_publisher.publish(json.dumps(authenticated_op))
    else:
        mqtt_publisher.publish()


speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained(model_name='titanet_large')
mqtt_subscriber = MqttSubscriber('localhost', 'Verification Module Input', 'audio/verification_input')
mqtt_subscriber.client.on_message = on_message
mqtt_subscriber.subscribe()
