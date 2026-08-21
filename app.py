from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import traceback
import uuid

from llm import ask_llm
from context_builder import build_context

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)

# --------------------------------------------------
# IN-MEMORY CONVERSATION STORAGE
# --------------------------------------------------

conversations = {}

MAX_HISTORY_MESSAGES = 10


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# --------------------------------------------------
# CHAT API
# --------------------------------------------------

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(force=True)

        user_message = data.get("message", "").strip()

        # Accept either naming style from frontend
        conversation_id = (
            data.get("conversation_id")
            or data.get("conversationId")
        )

        # --------------------------------------------------
        # EMPTY MESSAGE
        # --------------------------------------------------

        if not user_message:
            return jsonify({
                "reply": "Please type a farming related question."
            }), 200

        # --------------------------------------------------
        # CREATE CONVERSATION ID IF NEEDED
        # --------------------------------------------------

        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        # --------------------------------------------------
        # GET EXISTING HISTORY
        # --------------------------------------------------

        history = conversations.get(conversation_id, [])

        print("=" * 50)
        print("FARMFLUENCE CHAT")
        print("CONVERSATION ID:", conversation_id)
        print("HISTORY MESSAGES:", len(history))
        print("USER:", user_message)
        print("=" * 50)

        # --------------------------------------------------
        # HANDLE SIMPLE VAGUE INPUTS
        # --------------------------------------------------

        vague_inputs = [
            "yes",
            "ok",
            "okay",
            "haan",
            "ha",
            "hmm",
            "okok"
        ]

        if user_message.lower() in vague_inputs:

            reply = (
                "Sure. What would you like help with?\n"
                "1. Crop management\n"
                "2. Irrigation guidance\n"
                "3. Pest and disease management\n"
                "4. Fertigation and nutrition\n"
                "5. Talk to an expert"
            )

        else:

            # --------------------------------------------------
            # BUILD COMPLETE CONTEXT
            # --------------------------------------------------

            messages = build_context(
                user_message=user_message,
                history=history
            )

            # --------------------------------------------------
            # CALL LLM
            # --------------------------------------------------

            reply = ask_llm(messages)

        # --------------------------------------------------
        # SAVE USER MESSAGE
        # --------------------------------------------------

        history.append({
            "role": "user",
            "content": user_message
        })

        # --------------------------------------------------
        # SAVE ASSISTANT RESPONSE
        # --------------------------------------------------

        history.append({
            "role": "assistant",
            "content": reply
        })

        # --------------------------------------------------
        # LIMIT HISTORY
        # --------------------------------------------------

        if len(history) > MAX_HISTORY_MESSAGES:
            history = history[-MAX_HISTORY_MESSAGES:]

        conversations[conversation_id] = history

        # --------------------------------------------------
        # RETURN RESPONSE
        # --------------------------------------------------

        return jsonify({
            "reply": reply,
            "conversation_id": conversation_id
        }), 200

    except Exception as e:

        print("ERROR in /chat:", e)
        traceback.print_exc()

        return jsonify({
            "reply": "FarmFluence AI is currently unavailable. Please try again in a few moments."
        }), 500


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    print(">>> FarmFluence server running <<<")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
