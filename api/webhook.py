from backend import get_chat_response

def handler(request):
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        token = request.args.get("hub.verify_token")

        if mode == "subscribe" and token == "mysupersecrettoken123":
            return challenge
        return "Verification failed", 403

    if request.method == "POST":
        data = request.json

        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message["from"]
            text = message["text"]["body"]

            reply_text = get_chat_response(text)

            send_whatsapp_message(sender, reply_text)

        except Exception as e:
            print("Error:", e)

        return "OK"


import requests

WHATSAPP_TOKEN = "EAAh9SgXEeD4BQB2rwg9zPqZBX8irZCEozWFJAjZBxJk7xcafHOMrggirXeC2fY1yRTBiJHI5Ut6HkTiO0N8apCif5LKQ1DvLOHUk7Syi1oluGOpivJZBfRQGqN5rjEaQM2XmSUOQZAVT3OFloRNYwq7K463PWzgsmzCZABELRKcfv6ouefZBexVtZCWmKxuRQT3YmQZDZD"
PHONE_NUMBER_ID = "892587860611406"

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
