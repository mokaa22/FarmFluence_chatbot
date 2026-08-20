import os
import re
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not configured")

client = Groq(api_key=GROQ_API_KEY)


def clean_response(text):
    """
    Remove Qwen reasoning/thinking content before
    sending the response to the FarmFluence chatbot.
    """

    if not text:
        return ""

    # Remove complete <think>...</think> blocks
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    # If only a closing </think> remains
    text = re.sub(
        r"</think>",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove an opening <think> if it remains
    text = re.sub(
        r"<think>",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove common reasoning marker
    text = re.sub(
        r"\[Proceeds\]",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Clean excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def ask_llm(messages):

    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=messages,
        reasoning_effort="none",
        reasoning_format="hidden",
        temperature=0.7,
        max_tokens=1024
    )

    raw_reply = response.choices[0].message.content

    # Clean any reasoning accidentally returned by the model
    reply = clean_response(raw_reply)

    return reply
