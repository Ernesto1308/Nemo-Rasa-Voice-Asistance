import nemo.collections.asr as nemo_asr


model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(model_name="stt_es_conformer_transducer_large")
transcription = model.transcribe(["../audios/speech.wav"])[0][0]
print(transcription)
print(len(transcription))
