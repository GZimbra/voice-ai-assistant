from config import WAKE_WORD


def detect_wakeword(text):
    return WAKE_WORD.lower() in text.lower()
