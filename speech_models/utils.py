from datetime import datetime


def write_audio(data_bytes, audio):
    with open(audio, mode='wb') as aud:
        aud.write(data_bytes)
        aud.close()


def read_audio(audio):
    with open(audio, mode='rb') as text_speech:
        data_bytes = text_speech.read()
        text_speech.close()

    return data_bytes


def time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time
