import json

from flask import Blueprint, request

from acces_data_layer.services.older_person_service import select_all
from speech_models.models import VoiceAssistant
from utils import write_audio, time, serialize_bytes

# Define the endpoint for audio
bp = Blueprint('audio', __name__, url_prefix='/api/v1/audio')

sv_model = VoiceAssistant.get_model('SpeakerVerificationModel')
stt_model = VoiceAssistant.get_model('SpeechRecognitionModel')
tts_model = VoiceAssistant.get_model('TextToSpeechModel')


@bp.route('/verification_input', methods=['POST'])
def speaker_verification():
    print('Solicitud recibida', time())
    data = request.get_json()
    unknown_speaker_bytes = bytes(data['unknown_speaker'])
    write_audio(unknown_speaker_bytes, 'audios/unknown_speaker.wav')
    authenticated_op = None
    old_person_list = select_all()

    for current_old_person in old_person_list:
        write_audio(current_old_person.audio, 'audios/known_speaker.wav')

        if sv_model.run(known_audio='audios/known_speaker.wav', unknown_audio='audios/unknown_speaker.wav'):
            authenticated_op = current_old_person
            break

    print('Enviando respuesta', time())
    if authenticated_op:
        authenticated_op = authenticated_op.to_dict()
        authenticated_op['audio'] = data['unknown_speaker']
        return json.dumps(authenticated_op), 200
    else:
        return json.dumps({"id_older_person": 0}), 200


@bp.route('/speech_rec_input', methods=['POST'])
def speech_to_text():
    print('Solicitud recibida', time())
    data = request.get_json()
    known_speaker = bytes(data['audio'])
    audio_path = 'audios/speech_to_text.wav'
    write_audio(known_speaker, audio_path)
    text = stt_model.run(audio_path=audio_path)
    print('Enviando respuesta', time())
    return json.dumps({
        "id_older_person": data["id_older_person"],
        "older_person_name": data["older_person_name"],
        "text": text,
    }), 200


@bp.route('/text_to_speech_input', methods=['POST'])
def text_to_speech():
    print('Solicitud recibida', time())
    data = request.get_data(as_text=True)
    audio_bytes = tts_model.run(text=data)
    audio_serialized = serialize_bytes(audio_bytes)
    print('Enviando respuesta', time())
    return json.dumps({"audio": audio_serialized}), 200
