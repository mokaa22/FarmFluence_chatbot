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
# Health Check (for Render wake-up)
# ---------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ---------------------------
# Chat API
# ---------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Please type a farming-related question 🌱"
            })

        # Build system + user context
        messages = build_context(user_message)

        # Call LLM
        reply = ask_llm(messages)

        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ ERROR in /chat:", e)
        traceback.print_exc()
        return jsonify({
            "reply": "⚠️ Something went wrong. Please try again."
        }), 500


# ---------------------------
# Run locally only
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    print(">>> FarmFluence server running <<<")
    app.run(debug=True)
