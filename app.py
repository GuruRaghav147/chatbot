from flask import Flask, request, jsonify
from backend import get_chat_response
import requests

app = Flask(__name__)

VERIFY_TOKEN =  "mysupersecrettoken123"
WHATSAPP_TOKEN = "EAAh9SgXEeD4BQB2rwg9zPqZBX8irZCEozWFJAjZBxJk7xcafHOMrggirXeC2fY1yRTBiJHI5Ut6HkTiO0N8apCif5LKQ1DvLOHUk7Syi1oluGOpivJZBfRQGqN5rjEaQM2XmSUOQZAVT3OFloRNYwq7K463PWzgsmzCZABELRKcfv6ouefZBexVtZCWmKxuRQT3YmQZDZD"
PHONE_NUMBER_ID = "892587860611406"   

# Webhook verification
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    token = request.args.get("hub.verify_token")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403


# Receive incoming messages
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"]

        reply_text = bot_reply(text)    # Send to your chatbot

        send_whatsapp_message(sender, reply_text)
    except Exception as e:
        print("Error:", e)

        

    return "OK", 200


# Your chatbot logic
def bot_reply(user_msg):
    # Replace this with your actual Python EXE chatbot logic
    return get_chat_response(user_msg)


# Send message API
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

    requests.post(url, headers=headers, json=data)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
