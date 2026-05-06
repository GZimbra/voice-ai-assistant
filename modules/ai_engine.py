from modules.ml_intent import intent_classifier


def ask_ai(prompt, memory):
    intent = intent_classifier.predict(prompt)
    memory.add("user", prompt)

    answer = LocalAssistantEngine(memory).answer(prompt, intent)
    memory.add("assistant", answer)

    return answer


class LocalAssistantEngine:

    def __init__(self, memory):
        self.memory = memory

    def answer(self, prompt, intent):
        prompt_l = prompt.lower()

        if intent.label == "greeting":
            return "Online. Envie objetivo tecnico: codigo, rede, seguranca ou diagnostico."

        if intent.label == "summary":
            return self._summarize_context()

        if intent.label == "network":
            return self._network_answer(prompt_l, intent)

        if intent.label == "security":
            return self._security_answer(prompt_l, intent)

        if intent.label == "code":
            return self._code_answer(prompt_l, intent)

        return self._unknown_answer(intent)

    def _network_answer(self, prompt, intent):
        if "dns" in prompt:
            return "\n".join(
                [
                    f"Intencao: redes ({intent.confidence:.2f}).",
                    "Diagnostico: validar resolucao DNS, rota e conectividade.",
                    "Comandos Windows:",
                    "nslookup dominio.com",
                    "Resolve-DnsName dominio.com",
                    "ipconfig /all",
                    "tracert dominio.com",
                    "Test-NetConnection dominio.com -Port 443",
                    "Causa comum: DNS incorreto, cache local, bloqueio de firewall ou rota quebrada.",
                ]
            )

        if "porta" in prompt or "port" in prompt:
            return "\n".join(
                [
                    f"Intencao: redes ({intent.confidence:.2f}).",
                    "Diagnostico: verificar se a porta esta escutando e se ha bloqueio no caminho.",
                    "Comandos Windows:",
                    "netstat -ano | findstr LISTENING",
                    "Test-NetConnection 192.168.0.10 -Port 443",
                    "Get-NetTCPConnection -State Listen",
                    "Hardening: exponha somente portas necessarias e filtre por origem no firewall.",
                ]
            )

        return "\n".join(
            [
                f"Intencao: redes ({intent.confidence:.2f}).",
                "Checklist rapido:",
                "1. ipconfig /all",
                "2. ping gateway",
                "3. ping 8.8.8.8",
                "4. nslookup dominio.com",
                "5. tracert destino",
                "6. Test-NetConnection destino -Port porta",
            ]
        )

    def _security_answer(self, prompt, intent):
        if "brute" in prompt:
            return "\n".join(
                [
                    f"Intencao: seguranca ({intent.confidence:.2f}).",
                    "Mitigacao para brute force:",
                    "1. rate limit por IP e usuario",
                    "2. lockout progressivo com janela curta",
                    "3. MFA para contas sensiveis",
                    "4. logs de falha com IP, user-agent e ASN",
                    "5. alerta por pico de 401/403",
                    "6. senha com hash Argon2id ou bcrypt",
                    "Defesa adicional: bloquear credenciais vazadas e aplicar captcha apenas apos risco elevado.",
                ]
            )

        if "xss" in prompt:
            return "\n".join(
                [
                    f"Intencao: seguranca ({intent.confidence:.2f}).",
                    "XSS: validar entrada nao basta; encode a saida conforme contexto.",
                    "Mitigacao:",
                    "1. output encoding HTML/JS/URL",
                    "2. sanitizacao com allowlist para HTML rico",
                    "3. Content-Security-Policy restritiva",
                    "4. cookies HttpOnly, Secure e SameSite",
                    "5. evitar innerHTML/dangerouslySetInnerHTML",
                ]
            )

        return "\n".join(
            [
                f"Intencao: seguranca ({intent.confidence:.2f}).",
                "Analise minima:",
                "1. ativo afetado",
                "2. superficie exposta",
                "3. vetor de ataque",
                "4. impacto tecnico",
                "5. evidencia/log",
                "6. mitigacao imediata",
                "7. correcao definitiva",
            ]
        )

    def _code_answer(self, prompt, intent):
        if "python" in prompt:
            return "\n".join(
                [
                    f"Intencao: codigo ({intent.confidence:.2f}).",
                    "Para diagnosticar Python, envie traceback completo e versao:",
                    "python --version",
                    "pip freeze",
                    "python -m pip check",
                    "Padrao recomendado: isolar em venv, fixar dependencias e validar com py_compile/pytest.",
                ]
            )

        if ".net" in prompt or "csharp" in prompt or "c#" in prompt:
            return "\n".join(
                [
                    f"Intencao: codigo ({intent.confidence:.2f}).",
                    "Base para API .NET segura:",
                    "dotnet new webapi -n SecureApi",
                    "dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer",
                    "Aplicar: HTTPS, JWT curto, refresh token rotativo, rate limit e logs estruturados.",
                ]
            )

        return "\n".join(
            [
                f"Intencao: codigo ({intent.confidence:.2f}).",
                "Envie linguagem, erro completo, trecho minimo reproduzivel e comando executado.",
                "Sem isso, o diagnostico vira chute tecnico.",
            ]
        )

    def _summarize_context(self):
        messages = self.memory.get_messages()[1:]
        if not messages:
            return "Sem historico util ainda."

        last_items = messages[-6:]
        lines = ["Contexto recente:"]
        for item in last_items:
            role = "Usuario" if item["role"] == "user" else "Assistente"
            lines.append(f"{role}: {item['content'][:120]}")

        return "\n".join(lines)

    @staticmethod
    def _unknown_answer(intent):
        return "\n".join(
            [
                f"Intencao indefinida ({intent.confidence:.2f}).",
                "Envie um objetivo tecnico mais especifico.",
                "Formato ideal: alvo, erro/sintoma, ambiente, comando executado e resultado esperado.",
            ]
        )
