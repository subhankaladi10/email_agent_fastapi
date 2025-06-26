# filename: main.py
from fastapi import FastAPI, Request

app = FastAPI()

latest_reply = None

@app.route('/')
def index():
    return 'Webhook Running ✅'

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    incoming_msg = form.get("Body", "").strip()
    global latest_reply
    latest_reply = incoming_msg
    print(f"📥 WhatsApp reply received: {incoming_msg}")
    return {"status": "received"}
