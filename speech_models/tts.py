import soundfile as sf
from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.models import HifiGanModel


fastpitch_name = "tts_es_fastpitch_multispeaker"
hifigan_name = "tts_es_hifigan_ft_fastpitch_multispeaker"
spec_generator = FastPitchModel.from_pretrained(fastpitch_name)
model = HifiGanModel.from_pretrained(hifigan_name)
print("MODEL LOADED")
payload_decoded = ("Estamos probando el rendimiento del modelo bajo diferentes escenarios. Son la una y quince de la tarde")
parsed = spec_generator.parse(payload_decoded, normalize=False)
speaker = 100
spectrogram = spec_generator.generate_spectrogram(tokens=parsed, speaker=speaker)
audio = model.convert_spectrogram_to_audio(spec=spectrogram)
audio = audio.detach().cpu().numpy()[0]
sample_rate = 44100
sf.write('../audios/speech.wav', audio, sample_rate)
print("DONE")
