<<<<<<< HEAD
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import traceback

from llm import ask_llm
from context_builder import build_context
from image_analysis import analyze_plant_image

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ================= CONFIG =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# =========================================


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- TEXT CHAT (LLM) ----------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please type a farming-related message 🌱"})

        # Build FarmFluence-controlled context
        messages = build_context(user_message)

        # Ask LLM
        reply = ask_llm(messages)

        return jsonify({"reply": reply})

    except Exception as e:
        print("CHAT ERROR:", e)
        traceback.print_exc()
        return jsonify({
            "reply": "⚠️ Something went wrong while processing your message. Please try again."
        })


# ---------- IMAGE UPLOAD & ANALYSIS ----------
@app.route("/upload-image", methods=["POST"])
def upload_image():
    try:
        if "image" not in request.files:
            return jsonify({"reply": "❌ No image received."})

        image = request.files["image"]

        if image.filename == "":
            return jsonify({"reply": "❌ No image selected."})

        if not allowed_file(image.filename):
            return jsonify({
                "reply": "❌ Please upload a clear plant image (JPG / PNG format)."
            })

        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

        # 🔍 REAL image analysis using Groq (LLaVA)
        image_reply = analyze_plant_image(image_path)

        # 🧹 Cleanup for privacy
        os.remove(image_path)

        return jsonify({"reply": image_reply})

    except Exception as e:
        print("IMAGE ANALYSIS ERROR:", e)
        traceback.print_exc()

        return jsonify({
            "reply": (
                "⚠️ I couldn't analyze this image properly.\n\n"
                "Please make sure:\n"
                "• The image is clear\n"
                "• Leaf or crop area is visible\n"
                "• Good lighting is available\n\n"
                "You may try uploading another image."
            )
        })


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
=======
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import traceback

from llm import ask_llm
from context_builder import build_context
from image_analysis import analyze_plant_image

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ================= CONFIG =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# =========================================


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- TEXT CHAT (LLM) ----------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please type a farming-related message 🌱"})

        # Build FarmFluence-controlled context
        messages = build_context(user_message)

        # Ask LLM
        reply = ask_llm(messages)

        return jsonify({"reply": reply})

    except Exception as e:
        print("CHAT ERROR:", e)
        traceback.print_exc()
        return jsonify({
            "reply": "⚠️ Something went wrong while processing your message. Please try again."
        })


# ---------- IMAGE UPLOAD & ANALYSIS ----------
@app.route("/upload-image", methods=["POST"])
def upload_image():
    try:
        if "image" not in request.files:
            return jsonify({"reply": "❌ No image received."})

        image = request.files["image"]

        if image.filename == "":
            return jsonify({"reply": "❌ No image selected."})

        if not allowed_file(image.filename):
            return jsonify({
                "reply": "❌ Please upload a clear plant image (JPG / PNG format)."
            })

        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

        # 🔍 REAL image analysis using Groq (LLaVA)
        image_reply = analyze_plant_image(image_path)

        # 🧹 Cleanup for privacy
        os.remove(image_path)

        return jsonify({"reply": image_reply})

    except Exception as e:
        print("IMAGE ANALYSIS ERROR:", e)
        traceback.print_exc()

        return jsonify({
            "reply": (
                "⚠️ I couldn't analyze this image properly.\n\n"
                "Please make sure:\n"
                "• The image is clear\n"
                "• Leaf or crop area is visible\n"
                "• Good lighting is available\n\n"
                "You may try uploading another image."
            )
        })


# ---------- RUN ----------
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# routes here...

>>>>>>> c9f2407 (Fix project structure for Render deployment)
