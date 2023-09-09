import soundfile as sf
from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.models import HifiGanModel
from mqtt_provider import MqttPublisher, MqttSubscriber
from utils import read_audio


def on_message(client, userdata, message):
    payload_decoded = message.payload.decode('utf-8')
    mqtt_publish = MqttPublisher('localhost', 'TextToSpeech Module Output', 'audio/text_to_speech_output')
    parsed = spec_generator.parse(payload_decoded, normalize=False)
    speaker = 1
    spectrogram = spec_generator.generate_spectrogram(tokens=parsed, speaker=speaker)
    audio = model.convert_spectrogram_to_audio(spec=spectrogram)
    audio = audio.detach().cpu().numpy()[0]
    sample_rate = 44100
    sf.write('../audios/speech.wav', audio, sample_rate)
    mqtt_publish.publish(read_audio('../audios/speech.wav'))


fastpitch_name = "tts_es_fastpitch_multispeaker"
hifigan_name = "tts_es_hifigan_ft_fastpitch_multispeaker"
spec_generator = FastPitchModel.from_pretrained(fastpitch_name)
model = HifiGanModel.from_pretrained(hifigan_name)
mqtt_subscribe = MqttSubscriber('localhost', 'TextToSpeech Module Input', 'audio/text_to_speech_input')
mqtt_subscribe.client.on_message = on_message
mqtt_subscribe.subscribe()
