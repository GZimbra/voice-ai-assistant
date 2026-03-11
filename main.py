from modules.recorder import record_audio
from modules.speech_to_text import transcribe
from modules.ai_engine import ask_ai
from modules.tts_engine import speak
from modules.wakeword import detect_wakeword
from modules.conversation_memory import ConversationMemory

from rich import print

memory = ConversationMemory()

def main():

    print("\n[bold green]Assistente de Voz iniciado[/bold green]\n")

    while True:

        audio = record_audio()

        text = transcribe(audio)

        if text == "":
            continue

        print("[cyan]Você disse:[/cyan]", text)

        if "sair" in text.lower():
            print("Encerrando...")
            break

        if detect_wakeword(text):

            question = text.replace("hacker", "")

            answer = ask_ai(question, memory)

            print("[yellow]IA:[/yellow]", answer)

            speak(answer)

        else:

            print("Aguardando palavra de ativação...")

if __name__ == "__main__":
    main()