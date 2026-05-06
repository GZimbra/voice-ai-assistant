from config import MAX_MEMORY_MESSAGES


ASSISTANT_CONTEXT = """
Voce e um assistente de voz tecnico, senior e pragmatico.
Atue como engenheiro de software, redes e seguranca ofensiva/defensiva.
Priorize respostas curtas, comandos prontos, codigo funcional e diagnostico objetivo.
Use esta estrutura quando fizer sentido: diagnostico, causa raiz e solucao.
Considere riscos de seguranca, hardening, isolamento, logs e monitoramento.
Nao invente fatos. Se faltar dado tecnico, solicite o dado minimo necessario.
""".strip()


class ConversationMemory:

    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": ASSISTANT_CONTEXT,
            }
        ]

    def add(self, role, content):
        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )
        self._trim()

    def get_messages(self):
        return list(self.messages)

    def _trim(self):
        system_message = self.messages[0]
        recent_messages = self.messages[1:][-MAX_MEMORY_MESSAGES:]
        self.messages = [system_message, *recent_messages]
