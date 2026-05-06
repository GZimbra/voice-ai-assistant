import re
from dataclasses import dataclass

from config import INTENT_CONFIDENCE_THRESHOLD


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_#+.-]+")

TRAINING_DATA = [
    ("ola bom dia", "greeting"),
    ("oi tudo bem", "greeting"),
    ("hacker voce esta ai", "greeting"),
    ("explique esse codigo python", "code"),
    ("crie uma api em csharp dotnet", "code"),
    ("corrija esse erro no script", "code"),
    ("gere um comando powershell", "code"),
    ("analise esse traceback", "code"),
    ("como configurar vlan no switch", "network"),
    ("diagnostique perda de pacote", "network"),
    ("qual porta esta aberta", "network"),
    ("como testar dns e gateway", "network"),
    ("explique tcp udp firewall nat", "network"),
    ("como fazer hardening linux", "security"),
    ("analise vulnerabilidade xss", "security"),
    ("monte um checklist de pentest", "security"),
    ("como mitigar brute force", "security"),
    ("revise risco de seguranca", "security"),
    ("resuma nossa conversa", "summary"),
    ("o que voce lembra", "summary"),
    ("sair encerrar finalizar", "exit"),
    ("pare o assistente", "exit"),
]

INTENT_HINTS = {
    "greeting": "cumprimento; responda curto e peca o objetivo tecnico",
    "code": "programacao; priorize codigo, comandos e diagnostico de erro",
    "network": "redes; considere camadas OSI, conectividade, DNS, rotas, portas e firewall",
    "security": "seguranca; considere ameacas, impacto, explorabilidade e mitigacao defensiva",
    "summary": "memoria; sintetize contexto e proximos passos",
    "exit": "encerramento; finalize sem executar acoes adicionais",
    "unknown": "indefinido; peca o dado tecnico minimo se a pergunta estiver vaga",
}


@dataclass(frozen=True)
class IntentResult:
    label: str
    confidence: float
    hint: str


class _FallbackIntentClassifier:

    KEYWORDS = {
        "security": ("vulnerabilidade", "pentest", "exploit", "hardening", "xss", "sql injection", "firewall"),
        "network": ("rede", "dns", "tcp", "udp", "porta", "gateway", "vlan", "nat", "pacote"),
        "code": ("codigo", "python", "c#", "csharp", ".net", "script", "erro", "api", "powershell"),
        "summary": ("resuma", "lembra", "contexto"),
        "exit": ("sair", "encerrar", "finalizar", "pare"),
    }

    def predict(self, text):
        normalized = text.lower()

        for label, keywords in self.KEYWORDS.items():
            if any(keyword in normalized for keyword in keywords):
                return IntentResult(label, 0.50, INTENT_HINTS[label])

        return IntentResult("unknown", 0.0, INTENT_HINTS["unknown"])


class TorchIntentClassifier:

    def __init__(self):
        self.available = False
        self.labels = sorted({label for _, label in TRAINING_DATA})
        self.vocabulary = self._build_vocabulary(TRAINING_DATA)
        self.fallback = _FallbackIntentClassifier()

        try:
            import torch
            from torch import nn
        except ImportError:
            self.torch = None
            self.model = None
            return

        self.torch = torch
        self.torch.manual_seed(7)
        self.model = nn.Sequential(
            nn.Linear(len(self.vocabulary), 32),
            nn.ReLU(),
            nn.Linear(32, len(self.labels)),
        )
        self._train()
        self.available = True

    def predict(self, text):
        if not self.available:
            return self.fallback.predict(text)

        with self.torch.no_grad():
            vector = self._vectorize(text).unsqueeze(0)
            logits = self.model(vector)
            probabilities = self.torch.softmax(logits, dim=1).squeeze(0)
            confidence, index = self.torch.max(probabilities, dim=0)

        label = self.labels[index.item()]
        confidence_value = float(confidence.item())

        if confidence_value < INTENT_CONFIDENCE_THRESHOLD:
            label = "unknown"

        return IntentResult(label, confidence_value, INTENT_HINTS[label])

    def _train(self):
        x_train = self.torch.stack([self._vectorize(text) for text, _ in TRAINING_DATA])
        y_train = self.torch.tensor([self.labels.index(label) for _, label in TRAINING_DATA])

        optimizer = self.torch.optim.Adam(self.model.parameters(), lr=0.03)
        loss_fn = self.torch.nn.CrossEntropyLoss()

        self.model.train()
        for _ in range(350):
            optimizer.zero_grad()
            output = self.model(x_train)
            loss = loss_fn(output, y_train)
            loss.backward()
            optimizer.step()

        self.model.eval()

    def _vectorize(self, text):
        tokens = set(self._tokenize(text))
        values = [1.0 if token in tokens else 0.0 for token in self.vocabulary]
        return self.torch.tensor(values, dtype=self.torch.float32)

    @staticmethod
    def _build_vocabulary(data):
        tokens = set()
        for text, _ in data:
            tokens.update(TorchIntentClassifier._tokenize(text))
        return sorted(tokens)

    @staticmethod
    def _tokenize(text):
        return TOKEN_PATTERN.findall(text.lower())


intent_classifier = TorchIntentClassifier()
