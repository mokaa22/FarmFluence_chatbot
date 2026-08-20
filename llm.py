import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not configured")

client = Groq(api_key=GROQ_API_KEY)


def ask_llm(messages):

    # TEMPORARY DIAGNOSTIC
    try:
        models = client.models.list()
        available_models = [m.id for m in models.data]
        print("========== GROQ AVAILABLE MODELS ==========")
        print(available_models)
        print("===========================================")
    except Exception as e:
        print("❌ Could not list Groq models:", e)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.5,
        max_tokens=1024
    )

    return response.choices[0].message.content
