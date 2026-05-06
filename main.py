import re

from rich import print

from config import WAKE_WORD
from modules.ai_engine import ask_ai
from modules.conversation_memory import ConversationMemory
from modules.ml_intent import intent_classifier
from modules.recorder import record_audio
from modules.speech_to_text import transcribe
from modules.tts_engine import speak
from modules.wakeword import detect_wakeword


memory = ConversationMemory()


def main():
    print("\n[bold green]Assistente de Voz iniciado[/bold green]")
    print(f"[dim]Palavra de ativacao: {WAKE_WORD}[/dim]\n")

    while True:
        audio = record_audio()
        text = transcribe(audio)

        if not text:
            continue

        print("[cyan]Voce disse:[/cyan]", text)

        intent = intent_classifier.predict(text)
        if intent.label == "exit" or "sair" in text.lower():
            print("[yellow]Encerrando...[/yellow]")
            break

        if not detect_wakeword(text):
            print("[dim]Aguardando palavra de ativacao...[/dim]")
            continue

        question = _remove_wakeword(text)
        answer = ask_ai(question, memory)

        print("[yellow]IA:[/yellow]", answer)
        speak(answer)


def _remove_wakeword(text):
    return re.sub(re.escape(WAKE_WORD), "", text, flags=re.IGNORECASE).strip()


if __name__ == "__main__":
    main()
