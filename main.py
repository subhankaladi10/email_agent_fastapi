from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Store for latest WhatsApp reply
latest_reply = None

class Reply(BaseModel):
    reply: str

@app.post("/webhook")
async def receive_reply(reply: Reply):
    global latest_reply
    latest_reply = reply.reply
    return {"status": "received"}

@app.get("/latest")
def get_latest_reply():
    return {"reply": latest_reply if latest_reply else "No reply found"}

@app.post("/reset")
def reset_reply():
    global latest_reply
    latest_reply = None
    return {"status": "reset"}
