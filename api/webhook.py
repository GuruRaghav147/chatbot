import json
import requests
from backend import get_chat_response   # your bot logic

VERIFY_TOKEN = "mysupersecrettoken123"
WHATSAPP_TOKEN = "EAAh9SgXEeD4BQB2rwg9zPqZBX8irZCEozWFJAjZBxJk7xcafHOMrggirXeC2fY1yRTBiJHI5Ut6HkTiO0N8apCif5LKQ1DvLOHUk7Syi1oluGOpivJZBfRQGqN5rjEaQM2XmSUOQZAVT3OFloRNYwq7K463PWzgsmzCZABELRKcfv6ouefZBexVtZCWmKxuRQT3YmQZDZD"
PHONE_NUMBER_ID = "892587860611406"


def handler(request):
    # ----------------------------------
    # GET REQUEST → VERIFY WEBHOOK
    # ----------------------------------
    def handler(request):
        if request.method == "GET":
            mode = request.query_params.get("hub.mode")
            challenge = request.query_params.get("hub.challenge")
            token = request.query_params.get("hub.verify_token")


        if mode == "subscribe" and token == VERIFY_TOKEN:
            return {"status": 200, "body": challenge}

        return {"status": 403, "body": "Verification failed"}

    # ----------------------------------
    # POST REQUEST → RECEIVE MESSAGE
    # ----------------------------------
    if request.method == "POST":
        data = request.get_json()


        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message["from"]
            text = message["text"]["body"]

            #  Here is your bot logic
            reply_text = get_chat_response(text)

            # Send the reply
            send_whatsapp_message(sender, reply_text)

        except Exception as e:
            print("Error:", e)

        return {"status": 200, "body": "OK"}

    return {"status": 405, "body": "Method Not Allowed"}


# ----------------------------------------------
# SEND MESSAGE TO WHATSAPP API
# ----------------------------------------------
def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=payload)
