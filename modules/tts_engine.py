from pathlib import Path

from gtts import gTTS
from playsound import playsound


RESPONSE_AUDIO = Path("response.mp3")


def speak(text):
    tts = gTTS(text=text, lang="pt")
    tts.save(str(RESPONSE_AUDIO))
    playsound(str(RESPONSE_AUDIO))
