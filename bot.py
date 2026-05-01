from groq_ai import get_ai_response

# Stores conversation history for each user
user_sessions = {}

def handle_message(user_phone, user_message):
    # Create new session if user is new
    if user_phone not in user_sessions:
        user_sessions[user_phone] = {
            "history": [],
            "lead": {
                "phone": user_phone,
                "name": None,
                "email": None
            }
        }

    session = user_sessions[user_phone]

    # Add user message to history
    session["history"].append({
        "role": "user",
        "content": user_message
    })

    # Get AI response
    ai_reply = get_ai_response(session["history"])

    # Save AI reply to history
    session["history"].append({
        "role": "assistant",
        "content": ai_reply
    })

    # Try to extract lead info from conversation
    extract_lead_info(user_message, session["lead"])

    # Check if we have complete lead
    lead_complete = all([
        session["lead"]["name"],
        session["lead"]["email"],
        session["lead"]["phone"]
    ])

    return ai_reply, session["lead"], lead_complete


def extract_lead_info(message, lead):
    import re

    # Extract email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, message)
    if email_match and not lead["email"]:
        lead["email"] = email_match.group()

    # Extract phone number
    phone_pattern = r'(\+91|0)?[6-9]\d{9}'
    phone_match = re.search(phone_pattern, message)
    if phone_match and not lead["phone"]:
        lead["phone"] = phone_match.group()

    # Simple name detection (if message is short and has no special chars)
    if not lead["name"]:
        message = message.strip()
        if (len(message.split()) <= 4 and
            message.replace(" ", "").isalpha() and
            len(message) > 3):
            lead["name"] = message.title()