from flask import Flask, request, jsonify
from backend import get_chat_response
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot Running Successfully!", 200


# ----------------------------------------------------
# GET REQUEST → META WEBHOOK VERIFICATION
# ----------------------------------------------------
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    token = request.args.get("hub.verify_token")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403


# ----------------------------------------------------
# POST REQUEST → RECEIVE MESSAGES
# ----------------------------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"]

        reply = get_chat_response(text)

        send_whatsapp_message(sender, reply)

    except Exception as e:
        print("ERROR:", e)

    return "OK", 200


# ----------------------------------------------------
# SEND MESSAGE BACK TO WHATSAPP
# ----------------------------------------------------
def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }

    try:
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        print("Send Error:", e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
