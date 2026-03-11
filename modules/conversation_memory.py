class ConversationMemory:

    def __init__(self):

        self.messages = [
            {
                "role": "system",
                "content": "Você é um assistente de voz especializado em tecnologia e segurança."
            }
        ]

    def add(self, role, content):

        self.messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self):

        return self.messages