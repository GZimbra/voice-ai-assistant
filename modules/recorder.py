import sounddevice as sd
from scipy.io.wavfile import write

from config import AUDIO_DURATION


def record_audio(filename="audio.wav", fs=44100):
    print("Escutando...")
    audio = sd.rec(int(AUDIO_DURATION * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)

    return filename
