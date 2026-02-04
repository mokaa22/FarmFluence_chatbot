from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import traceback

from llm import ask_llm
from context_builder import build_context

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please type a farming-related message 🌱"})

        messages = build_context(user_message)
        reply = ask_llm(messages)

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        return jsonify({"reply": "⚠️ Error occurred"})

if __name__ == "__main__":
    print(">>> FarmFluence server running <<<")
    app.run(debug=True)
