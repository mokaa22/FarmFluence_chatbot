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


# ============================================================
# IN-MEMORY CONVERSATION STORAGE
# ============================================================

conversation_store = {}


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    }), 200


# ============================================================
# CHAT API
# ============================================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(force=True) or {}

        user_message = str(
            data.get("message", "")
        ).strip()

        # ----------------------------------------------------
        # GET OR CREATE CONVERSATION ID
        # ----------------------------------------------------

        conversation_id = data.get("conversation_id")

        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        # ----------------------------------------------------
        # EMPTY MESSAGE
        # ----------------------------------------------------

        if not user_message:

            return jsonify({
                "reply": "Please type a farming related question.",
                "conversation_id": conversation_id
            }), 200

        # ----------------------------------------------------
        # GET EXISTING HISTORY
        # ----------------------------------------------------

        history = conversation_store.get(
            conversation_id,
            []
        )

        # ----------------------------------------------------
        # LOGGING
        # ----------------------------------------------------

        print("\n")
        print("=" * 50)
        print("FARMFLUENCE CHAT")
        print("CONVERSATION ID:", conversation_id)
        print("HISTORY MESSAGES:", len(history))
        print("USER:", user_message)
        print("=" * 50)

        # ----------------------------------------------------
        # HANDLE SIMPLE VAGUE INPUTS
        # ----------------------------------------------------

        vague_inputs = {
            "yes",
            "ok",
            "okay",
            "haan",
            "ha",
            "hmm",
            "okok"
        }

        if user_message.lower() in vague_inputs:

            reply = (
                "Sure. What would you like help with?\n"
                "1. Crop management\n"
                "2. Irrigation guidance\n"
                "3. Pest and disease management\n"
                "4. Fertigation and nutrition\n"
                "5. Talk to an expert"
            )

            # Save conversation
            history.append({
                "role": "user",
                "content": user_message
            })

            history.append({
                "role": "assistant",
                "content": reply
            })

            conversation_store[conversation_id] = history

            return jsonify({
                "reply": reply,
                "conversation_id": conversation_id
            }), 200

        # ----------------------------------------------------
        # BUILD LLM CONTEXT
        # ----------------------------------------------------

        messages = build_context(
            user_message=user_message,
            history=history
        )

        # ----------------------------------------------------
        # CALL LLM
        # ----------------------------------------------------

        reply = ask_llm(messages)

        # ----------------------------------------------------
        # SAVE CURRENT CONVERSATION
        # ----------------------------------------------------

        history.append({
            "role": "user",
            "content": user_message
        })

        history.append({
            "role": "assistant",
            "content": reply
        })

        # Keep only the latest 8 messages in server memory
        # to avoid unlimited memory growth.
        conversation_store[conversation_id] = history[-8:]

        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return jsonify({
            "reply": reply,
            "conversation_id": conversation_id
        }), 200

    except Exception as e:

        print("ERROR IN /chat:")
        print(str(e))

        traceback.print_exc()

        return jsonify({
            "reply": "FarmFluence AI is currently unavailable. Please try again in a few moments."
        }), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print(">>> FarmFluence AI server running <<<")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
