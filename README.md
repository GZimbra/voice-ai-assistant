# Local Voice AI Assistant

Local voice assistant built with Python for technical diagnostics and cybersecurity-oriented support.

- Local speech transcription with Whisper
- Configurable wake word
- Local neural intent classifier with PyTorch
- Offline technical response engine
- Short conversation memory
- No OpenAI API, no ChatGPT, no external AI provider

## Architecture

```text
Audio -> Local Whisper -> PyTorch Intent Classifier -> LocalAssistantEngine -> TTS
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

## Usage Examples

```text
hacker analyze an XSS vulnerability
hacker how to test DNS and gateway on Windows
hacker create a C# .NET API
hacker how to mitigate brute force attacks
hacker summarize our conversation
```

## Local AI

`modules/ml_intent.py` trains a PyTorch model at runtime:

- Input: bag-of-words from the transcribed sentence
- Architecture: `Linear -> ReLU -> Linear`
- Output: classified intent

Supported intents:

- `code`
- `network`
- `security`
- `summary`
- `greeting`
- `exit`
- `unknown`

`modules/ai_engine.py` uses the classified intent to generate local technical responses for:

- Python
- C#/.NET
- networking
- cybersecurity
- operational diagnostics

## Important Note

The package `openai-whisper` is used only for local Whisper transcription.

This project does not call the OpenAI API or any external AI provider.

