import os
import requests
from flask import Flask, request
from google import genai
from google.genai import types

app = Flask(__name__)
client = genai.Client(api_key=os.environ["AQ.Ab8RN6JJpJFKkmZwSZ2citwCK67mSUi9vrVqcoSb0Hn4f5TO4A"])
TOKEN = os.environ["TELEGRAM_TOKEN"]
SECRET = os.environ["WEBHOOK_SECRET"]

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != SECRET:
        return "forbidden", 403

    msg = (request.get_json() or {}).get("message", {})
    text = msg.get("text")
    chat_id = msg.get("chat", {}).get("id")

    if text and chat_id:
        try:
            cevap = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction="Kısa ve yardımcı cevaplar ver. Türkçe yaz.",
                    max_output_tokens=500,
                ),
            )
            yanit = cevap.text or "Cevap üretemedim."
        except Exception:
            yanit = "Şu an cevap veremiyorum, biraz sonra tekrar dene."

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": yanit},
            timeout=10,
        )
    return "ok"

@app.route("/")
def home():
    return "Bot çalışıyor"
