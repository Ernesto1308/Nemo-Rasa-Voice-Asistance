import nemo.collections.asr as nemo_asr

speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained('nvidia/speakerverification_en_titanet_large')
result = speaker_model.verify_speakers('../audios/known_speaker.wav', '../audios/unknown_speaker.wav')
