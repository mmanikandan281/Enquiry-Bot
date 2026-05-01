import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from dotenv import load_dotenv
from bot import handle_message
from sheets import save_lead

load_dotenv()

app = FastAPI()

# Twilio client
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def send_whatsapp(to, message):
    twilio_client.messages.create(
        from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
        to=to,
        body=message
    )

@app.get("/")
def root():
    return {"status": "QuAnHack Enquiry Bot is running! 🚀"}

@app.post("/webhook")
async def webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...)
):
    user_phone = From
    user_message = Body.strip()

    print(f"📩 Message from {user_phone}: {user_message}")

    # Get AI response and lead info
    ai_reply, lead, lead_complete = handle_message(user_phone, user_message)

    # Save lead to Google Sheets if complete
    if lead_complete:
        save_lead(lead)

    # printing ai reply
    print(f"🤖 AI Reply: {ai_reply}")

    # Send reply back via WhatsApp
    send_whatsapp(user_phone, ai_reply)

    return PlainTextResponse("OK", status_code=200)