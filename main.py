from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

latest_reply = None

@app.get("/", response_class=PlainTextResponse)
def index():
    return "Webhook Running ✅"

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    incoming_msg = form.get("Body", "").strip()
    global latest_reply
    latest_reply = incoming_msg
    print(f"📥 WhatsApp reply received: {incoming_msg}")
    return {"status": "received"}

@app.get("/latest")
def get_latest():
    return {"reply": latest_reply}
