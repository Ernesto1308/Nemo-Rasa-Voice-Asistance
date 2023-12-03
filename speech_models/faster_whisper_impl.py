from faster_whisper import WhisperModel

model_size = "large-v3"
model = WhisperModel(model_size)
segments, info = model.transcribe("../audios/speech_to_text.wav", language='es',beam_size=5)
my_string = ''.join([segment.text for segment in segments])
print(my_string)
