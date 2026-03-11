import whisper
from config import MODEL_WHISPER

model = whisper.load_model(MODEL_WHISPER)

def transcribe(audio_file):

    result = model.transcribe(audio_file)

    text = result["text"].strip()

    return text