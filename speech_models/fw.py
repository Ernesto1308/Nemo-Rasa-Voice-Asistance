from faster_whisper import WhisperModel

model_size = "large-v2"
model = WhisperModel(model_size)
segments, info = model.transcribe("../audios", beam_size=5)
my_string = ''.join([segment.text for segment in segments])
