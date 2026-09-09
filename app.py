import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.1-flash-lite"

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=GEMINI_API_KEY)

with open("chatbot_config.txt", "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read().strip()


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a travel question."}), 400

    try:
        prompt = f"{SYSTEM_PROMPT}\n\nUSER:\n{message}"

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        reply = (response.text or "").strip()

        if not reply:
            reply = "I couldn't generate a response right now."

        return jsonify({"reply": reply})

    except Exception:
        return jsonify({
            "error": "Sorry, I couldn't process your request right now."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
    )
