from abc import ABC, abstractmethod
from typing import Union

import numpy as np
from faster_whisper import WhisperModel
import nemo.collections.asr as nemo_asr
from nemo.collections.tts.models import FastPitchModel, HifiGanModel
import soundfile as sf

from utils import read_audio


class BaseModel(ABC):
    """Abstract base class for all model classes"""
    @abstractmethod
    def run(self, **kwargs) -> Union[str, bool, bytes]:
        """Abstract method to run model operation"""
        pass


class SpeechRecognitionModel(BaseModel):
    """Speech recognition model using Faster Whisper"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._speech_model = WhisperModel("large-v3")

    def run(self, audio_path: str) -> str:
        """Transcribe speech from audio file"""
        segments, info = self._speech_model.transcribe(audio=audio_path, beam_size=5, language='es')
        return "".join([s.text for s in segments])


class SpeakerVerificationModel(BaseModel):
    # Speaker recognition model using TitanNet
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained("titanet_large")

    def run(self, known_audio, unknown_audio) -> bool:
        # Verify speakers by comparing voices
        return self._speaker_model.verify_speakers(known_audio, unknown_audio)


class TextToSpeechModel(BaseModel):
    # Text-to-speech model using FastPitch and HifiGAN
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._spec_generator = FastPitchModel.from_pretrained("tts_es_fastpitch_multispeaker")
        self._vocoder = HifiGanModel.from_pretrained("tts_es_hifigan_ft_fastpitch_multispeaker")

    def run(self, text: str) -> bytes:
        # Generate speech audio from text and encode as base64
        speaker = 1
        text_list = text.split(',')
        audio_array = np.array([])

        for current_text in text_list:
            parsed = self._spec_generator.parse(current_text, normalize=False)
            spectrogram = self._spec_generator.generate_spectrogram(tokens=parsed, speaker=speaker)
            audio = self._vocoder.convert_spectrogram_to_audio(spec=spectrogram)
            audio = audio.detach().cpu().numpy()[0]
            # Append the generated audio to the audio array
            audio_array = np.concatenate((audio_array, audio))

        sample_rate = 44100
        sf.write('audios/speech.wav', audio_array, sample_rate)
        audio_bytes = read_audio('audios/speech.wav')
        return audio_bytes


class VoiceAssistant:
    @classmethod
    def get_model(cls, model_name: str) -> BaseModel:
        """Factory method to get a model instance"""
        try:
            model = globals()[model_name]()
        except KeyError:
            raise ValueError(f"Model '{model_name}' not implemented")

        return model

