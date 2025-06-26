# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# # Store for latest WhatsApp reply
# latest_reply = None

# class Reply(BaseModel):
#     reply: str

# @app.post("/webhook")
# async def receive_reply(reply: Reply):
#     global latest_reply
#     latest_reply = reply.reply
#     return {"status": "received"}

# @app.get("/latest")
# def get_latest_reply():
#     return {"reply": latest_reply if latest_reply else "No reply found"}

# @app.post("/reset")
# def reset_reply():
#     global latest_reply
#     latest_reply = None
#     return {"status": "reset"}


from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Allow CORS (optional for frontend/testing purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
latest_reply = None
latest_timestamp = None  # New: track when reply was received

@app.get("/", response_class=PlainTextResponse)
def index():
    return "Webhook Running ✅"

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    incoming_msg = form.get("Body", "").strip()

    global latest_reply, latest_timestamp
    latest_reply = incoming_msg
    latest_timestamp = datetime.utcnow()  # Save time in UTC
    print(f"📥 WhatsApp reply received at {latest_timestamp}: {incoming_msg}")

    return {"status": "received"}

@app.get("/latest")
def get_latest():
    return {
        "reply": latest_reply,
        "timestamp": latest_timestamp.isoformat() if latest_timestamp else None
    }

@app.post("/reset")
def reset_latest():
    global latest_reply, latest_timestamp
    latest_reply = None
    latest_timestamp = None
    print("🔄 /latest endpoint reset")
    return {"status": "reset"}
