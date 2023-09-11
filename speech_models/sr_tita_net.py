import json
import threading

import nemo.collections.asr as nemo_asr
from flask import Flask, request

from acces_data_layer.services import old_person_service
from utils import write_audio, time

app = Flask(__name__)


@app.route('/audio/verification_input', methods=['POST'])
def on_request():
    print('Solicitud recibida', time())
    data = request.get_json()
    unknown_speaker_bytes = bytes(data['unknown_speaker'])
    write_audio(unknown_speaker_bytes, '../audios/unknown_speaker.wav')
    authenticated_op = None
    old_person_list = old_person_service.select_all()

    for current_old_person in old_person_list:
        write_audio(current_old_person.audio, '../audios/known_speaker.wav')

        if speaker_model.verify_speakers('../audios/known_speaker.wav', '../audios/unknown_speaker.wav'):
            authenticated_op = current_old_person
            break

    print('Enviando respuesta', time())
    if authenticated_op:
        authenticated_op = authenticated_op.to_dict()
        authenticated_op['audio'] = data['unknown_speaker']
        return json.dumps(authenticated_op), 200
    else:
        return json.dumps({"id_old_person": 0}), 200


if __name__ == '__main__':
    speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained(model_name='titanet_large')
    app.run(host='0.0.0.0', port=8000)
