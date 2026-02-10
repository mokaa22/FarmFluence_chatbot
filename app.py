from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import traceback

from llm import ask_llm
from context_builder import build_context

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)

# ---------------------------
# Home Page
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------
# Health Check (Render / uptime)
# ---------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ---------------------------
# Chat API (USED BY WIDGET)
# ---------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        # 1️⃣ Empty input guard
        if not user_message:
            return jsonify({
                "reply": "Please type a farming-related question 🌱"
            })

        # 2️⃣ Handle vague replies BEFORE LLM
        vague_inputs = ["yes", "ok", "okay", "haan", "ha", "hmm", "okok"]

        if user_message.lower() in vague_inputs:
            return jsonify({
                "reply": (
                    "👍 No problem.\n"
                    "What would you like help with?\n"
                    "1️⃣ Crop management\n"
                    "2️⃣ Irrigation guidance\n"
                    "3️⃣ Pest & disease control\n"
                    "4️⃣ Bird protection methods\n"
                    "5️⃣ Talk to an expert"
                )
            })

        # 3️⃣ Build system + user context
        messages = build_context(user_message)

        # 4️⃣ Call LLM (Groq via llm.py)
        reply = ask_llm(messages)

        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ ERROR in /chat:", e)
        traceback.print_exc()
        return jsonify({
            "reply": "⚠️ Something went wrong. Please try again."
        }), 500


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    print(">>> FarmFluence server running <<<")
    app.run(host="0.0.0.0", port=5000, debug=True)
