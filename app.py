from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import traceback
import time

from llm import ask_llm
from context_builder import build_context

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)


# =========================================================
# CONVERSATION MEMORY
# =========================================================

# Stores chat history for active conversations.
# This is temporary in-memory storage.
conversation_history = {}

# Maximum number of messages stored per conversation.
# 20 messages = approximately 10 user + 10 assistant messages.
MAX_HISTORY_MESSAGES = 20

# Remove inactive conversations after 1 hour.
SESSION_TIMEOUT = 60 * 60


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    }), 200


# =========================================================
# CONVERSATION ID
# =========================================================

def get_conversation_id(data):
    """
    Get the conversation ID from the frontend.

    If the frontend does not provide one, create a temporary
    ID using the user's IP address and browser information.
    """

    conversation_id = data.get("conversation_id")

    if conversation_id:
        return conversation_id

    ip_address = request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    )

    user_agent = request.headers.get(
        "User-Agent",
        ""
    )

    return f"{ip_address}_{hash(user_agent)}"


# =========================================================
# CLEAN OLD CONVERSATIONS
# =========================================================

def cleanup_old_conversations():

    current_time = time.time()

    expired_sessions = []

    for conversation_id, conversation in conversation_history.items():

        last_activity = conversation.get(
            "last_activity",
            0
        )

        if current_time - last_activity > SESSION_TIMEOUT:
            expired_sessions.append(conversation_id)

    for conversation_id in expired_sessions:
        del conversation_history[conversation_id]


# =========================================================
# GET CONVERSATION HISTORY
# =========================================================

def get_history(conversation_id):

    cleanup_old_conversations()

    if conversation_id not in conversation_history:

        conversation_history[conversation_id] = {
            "messages": [],
            "last_activity": time.time()
        }

    conversation_history[conversation_id]["last_activity"] = time.time()

    return conversation_history[conversation_id]["messages"]


# =========================================================
# SAVE MESSAGE
# =========================================================

def save_message(
    conversation_id,
    role,
    content
):

    history = get_history(conversation_id)

    history.append({
        "role": role,
        "content": content
    })

    # Keep only the latest messages.
    if len(history) > MAX_HISTORY_MESSAGES:

        conversation_history[conversation_id]["messages"] = (
            history[-MAX_HISTORY_MESSAGES:]
        )


# =========================================================
# CHAT API
# =========================================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(force=True)

        if not data:
            return jsonify({
                "reply": "Please enter a message."
            }), 400

        user_message = data.get(
            "message",
            ""
        ).strip()

        # -------------------------------------------------
        # EMPTY MESSAGE
        # -------------------------------------------------

        if not user_message:

            return jsonify({
                "reply": "Please type a farming related question."
            }), 400


        # -------------------------------------------------
        # GET CONVERSATION
        # -------------------------------------------------

        conversation_id = get_conversation_id(data)

        history = get_history(
            conversation_id
        )


        # -------------------------------------------------
        # BUILD SYSTEM + HISTORY + CURRENT MESSAGE
        # -------------------------------------------------

        messages = build_context(
            user_message,
            history
        )


        # -------------------------------------------------
        # DEBUG INFORMATION
        # -------------------------------------------------

        print("\n========================================")
        print("FARMFLUENCE CHAT")
        print("CONVERSATION ID:", conversation_id)
        print("HISTORY MESSAGES:", len(history))
        print("USER:", user_message)
        print("========================================\n")


        # -------------------------------------------------
        # CALL GROQ
        # -------------------------------------------------

        reply = ask_llm(messages)


        # -------------------------------------------------
        # SAVE USER MESSAGE
        # -------------------------------------------------

        save_message(
            conversation_id,
            "user",
            user_message
        )


        # -------------------------------------------------
        # SAVE ASSISTANT RESPONSE
        # -------------------------------------------------

        save_message(
            conversation_id,
            "assistant",
            reply
        )


        # -------------------------------------------------
        # RETURN RESPONSE
        # -------------------------------------------------

        return jsonify({
            "reply": reply,
            "conversation_id": conversation_id
        }), 200


    except Exception as e:

        print("ERROR in /chat:", e)

        traceback.print_exc()

        return jsonify({
            "reply": (
                "FarmFluence AI is currently unavailable. "
                "Please try again in a few moments."
            )
        }), 500


# =========================================================
# CLEAR CHAT
# =========================================================

@app.route("/chat/clear", methods=["POST"])
def clear_chat():

    try:

        data = request.get_json(force=True)

        conversation_id = get_conversation_id(data)

        if conversation_id in conversation_history:

            del conversation_history[
                conversation_id
            ]

        return jsonify({
            "status": "cleared"
        }), 200


    except Exception as e:

        print(
            "ERROR clearing conversation:",
            e
        )

        return jsonify({
            "status": "error"
        }), 500


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    print(
        ">>> FarmFluence server running <<<"
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
