# flask_app.py
import os
from flask import Flask, request, jsonify
import requests
from backend import get_chat_response   # keep your backend import

app = Flask(__name__)

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    token = request.args.get("hub.verify_token")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message.get("text", {}).get("body", "")
        reply_text = bot_reply(text)
        send_whatsapp_message(sender, reply_text)
    except Exception:
        # log or ignore
        pass
    return "OK", 200

def bot_reply(user_msg):
    return get_chat_response(user_msg)

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=data)

# For Vercel deployment we don't call app.run() — Vercel will serve it.
