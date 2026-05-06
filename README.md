# Voice AI Assistant Local

Assistente de voz local em Python para diagnostico tecnico.

- transcricao local com Whisper
- wake word configuravel
- classificador neural local com PyTorch
- motor local de resposta tecnica
- memoria curta de conversa
- sem OpenAI, sem ChatGPT, sem API externa para IA

## Arquitetura

```text
Audio -> Whisper local -> PyTorch intent classifier -> LocalAssistantEngine -> TTS
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Executar

```powershell
python main.py
```

Exemplos:

```text
hacker analise uma vulnerabilidade xss
hacker como testar dns e gateway no windows
hacker crie uma api em csharp dotnet
hacker como mitigar brute force
hacker resuma nossa conversa
```

## IA local

`modules/ml_intent.py` treina em runtime um modelo PyTorch:

- entrada: bag-of-words da frase transcrita
- arquitetura: `Linear -> ReLU -> Linear`
- saida: intencao classificada

`modules/ai_engine.py` usa essa intencao para gerar resposta local com contexto tecnico de:

- Python
- C#/.NET
- redes
- ciberseguranca
- diagnostico operacional

Observacao: o pacote `openai-whisper` e usado apenas para Whisper local. Nao ha chamada para OpenAI API.
