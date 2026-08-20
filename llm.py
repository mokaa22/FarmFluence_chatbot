import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not configured")

client = Groq(api_key=GROQ_API_KEY)


def ask_llm(messages):
    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=messages,
        temperature=0.5,
        max_tokens=4096
    )

    return response.choices[0].message.content
