import numpy as np
import soundfile as sf
from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.models import HifiGanModel

fastpitch_name = "tts_es_fastpitch_multispeaker"
hifigan_name = "tts_es_hifigan_ft_fastpitch_multispeaker"
spec_generator = FastPitchModel.from_pretrained(fastpitch_name)
model = HifiGanModel.from_pretrained(hifigan_name)
speaker = 1
# Initialize an empty NumPy array to store the generated audio
audio_array = np.array([])
text = """ Tienes que tomar Paracetamol a las diez y treinta y cuatro de la mañana
y a las dos y veinticinco de la tarde, Duralgina a las once y cuarenta y cuatro de la mañana
y a las dos y veinticinco de la tarde, e Ibuprofeno a las diez y treinta y cuatro de la mañana
y a las dos y veinticinco de la tarde. 
"""
text_list = text.split(',')

for payload_decoded in text_list:
    parsed = spec_generator.parse(payload_decoded, normalize=False)
    spectrogram = spec_generator.generate_spectrogram(tokens=parsed, speaker=speaker)
    audio = model.convert_spectrogram_to_audio(spec=spectrogram)
    audio = audio.detach().cpu().numpy()[0]
    # Append the generated audio to the audio array
    audio_array = np.concatenate((audio_array, audio))

sample_rate = 44100
# Save the generated audio to a WAV file
sf.write('../audios/speech.wav', audio_array, sample_rate)
