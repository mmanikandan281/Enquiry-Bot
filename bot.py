from groq_ai import get_ai_response

# Stores conversation history for each user
user_sessions = {}

def handle_message(user_phone, user_message):
    # Create new session if user is new
    if user_phone not in user_sessions:
        user_sessions[user_phone] = {
            "history": [],
            "lead": {
                "phone": None,
                "name": None,
                "email": None
            },
            "collecting": False
        }

    session = user_sessions[user_phone]

    # Add user message to history
    session["history"].append({
        "role": "user",
        "content": user_message
    })

    # Get AI response FIRST
    ai_reply = get_ai_response(session["history"])

    # Save AI reply to history
    session["history"].append({
        "role": "assistant",
        "content": ai_reply
    })

    # Start collecting ONLY after AI asks for name/email/phone
    if any(word in ai_reply.lower() for word in ["full name", "email address", "phone number"]):
        session["collecting"] = True

    # Extract lead info only when collecting is True
    if session["collecting"]:
        extract_lead_info(user_message, session["lead"])

    # Check if lead is complete
    lead_complete = all([
        session["lead"]["name"],
        session["lead"]["email"],
        session["lead"]["phone"]
    ])

    if lead_complete:
        saved_lead = session["lead"].copy()
        # Reset for next lead
        session["lead"] = {
            "phone": user_phone.replace("whatsapp:", ""),
            "name": None,
            "email": None
        }
        session["collecting"] = False
        return ai_reply, saved_lead, True

    return ai_reply, session["lead"], False


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

    # Extract name
    if not lead["name"]:
        # Handle "Manikandan,email,phone" comma format
        parts = message.split(",")
        if len(parts) >= 2:
            first_part = parts[0].strip()
            if first_part.replace(" ", "").isalpha() and len(first_part) > 2:
                lead["name"] = first_part.title()
                return

        # Handle "my name is X" format
        name_match = re.search(
            r'(?:my name is|i am|name[:\s]+)\s*([A-Za-z ]{3,30})',
            message.lower()
        )
        if name_match:
            lead["name"] = name_match.group(1).strip().title()
            return

        # Handle short name only message like "Manikandan"
        words = message.strip().split()
        if (len(words) <= 3 and
            message.strip().replace(" ", "").isalpha() and
            len(message.strip()) > 2):
            lead["name"] = message.strip().title()