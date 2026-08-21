import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not configured")

client = Groq(api_key=GROQ_API_KEY)


def ask_llm(messages):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.6,
        max_completion_tokens=8192,
        include_reasoning=False
    )

    return response.choices[0].message.content
