import base64
import json

import soundfile as sf
from flask import Flask, request
from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.models import HifiGanModel

from utils import read_audio, time

app = Flask(__name__)


@app.route('/audio/text_to_speech_input', methods=['POST'])
def on_request():
    print('Solicitud recibida', time())
    data = request.get_data(as_text=True)
    parsed = spec_generator.parse(data, normalize=False)
    speaker = 1
    spectrogram = spec_generator.generate_spectrogram(tokens=parsed, speaker=speaker)
    audio = model.convert_spectrogram_to_audio(spec=spectrogram)
    audio = audio.detach().cpu().numpy()[0]
    sample_rate = 44100
    sf.write('../audios/speech.wav', audio, sample_rate)
    data = base64.b64encode(read_audio('../audios/speech.wav')).decode('utf-8')
    print('Enviando respuesta', time())
    return json.dumps({"audio": data}), 200


if __name__ == '__main__':
    fastpitch_name = "tts_es_fastpitch_multispeaker"
    hifigan_name = "tts_es_hifigan_ft_fastpitch_multispeaker"
    spec_generator = FastPitchModel.from_pretrained(fastpitch_name)
    model = HifiGanModel.from_pretrained(hifigan_name)
    app.run(host='0.0.0.0', port=8002)
