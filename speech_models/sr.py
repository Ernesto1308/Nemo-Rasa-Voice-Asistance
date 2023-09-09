import nemo.collections.asr as nemo_asr
from acces_data_layer.services import old_person_service
from speech_models.utils import write_audio

old_person_list = old_person_service.select()
speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained(model_name='titanet_large')

for current_old_person in old_person_list:
    write_audio(current_old_person.audio, '../audios/known_speaker.wav')

    if speaker_model.verify_speakers('../audios/known_speaker.wav', '../audios/unknown_speaker.wav'):
        print(current_old_person)
        break
