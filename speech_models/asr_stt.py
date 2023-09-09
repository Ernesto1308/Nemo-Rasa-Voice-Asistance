import nemo.collections.asr as nemo_asr
from mqtt_provider import MqttSubscriber, MqttPublisher
from utils import write_audio, time


def on_message(client, userdata, message):
    print('Solicitud recibida', time())
    payload_decoded = eval(message.payload.decode('utf-8'))
    unknown_speaker = bytes(payload_decoded['unknown_speaker'])
    write_audio(unknown_speaker, 'audios/speech_to_text.wav')
    transcription = model.transcribe(["audios/speech.wav"])[0][0]
    mqtt_publish = MqttPublisher('localhost', 'Speech Rec Module Output', 'audio/speech_rec_output')
    mqtt_publish.publish(transcription)


model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(model_name="stt_es_conformer_transducer_large")
mqtt_subscribe = MqttSubscriber('localhost', 'Speech Rec Module Input', 'audio/speech_rec_input')
mqtt_subscribe.client.on_message = on_message
mqtt_subscribe.subscribe()
