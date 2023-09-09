from faster_whisper import WhisperModel
from docx import Document

model_size = "large-v2"
model = WhisperModel(model_size)
segments, info = model.transcribe("../audios", beam_size=5)
my_string = ''.join([segment.text for segment in segments])
document = Document()
document.add_paragraph(my_string)
document.save('my_string.docx')
