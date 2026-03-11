from config import WAKE_WORD

def detect_wakeword(text):

    if WAKE_WORD.lower() in text.lower():

        return True

    return False