import json

from faster_whisper import WhisperModel
from flask import Flask, request

from utils import write_audio, time

app = Flask(__name__)


@app.route('/audio/speech_rec_input', methods=['POST'])
def on_request():
    print('Solicitud recibida', time())
    data = request.get_json()
    known_speaker = bytes(data['audio'])
    write_audio(known_speaker, '../audios/speech_to_text.wav')
    segments, info = model.transcribe("../audios/speech_to_text.wav", beam_size=5)
    my_string = ''.join([segment.text for segment in segments])
    print('Enviando respuesta', time())
    return json.dumps({
        "id_old_person": data["id_old_person"],
        "old_person_name": data["old_person_name"],
        "text": my_string,
    }), 200


if __name__ == '__main__':
    model_size = "large-v2"
    model = WhisperModel(model_size)
    app.run(host='0.0.0.0', port=8001)
