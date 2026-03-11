from openai import OpenAI
from config import OPENAI_API_KEY, CHAT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_ai(prompt, memory):

    messages = memory.get_messages()

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages
    )

    answer = response.choices[0].message.content

    memory.add("assistant", answer)

    return answer