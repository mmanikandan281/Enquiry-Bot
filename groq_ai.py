import os
from groq import Groq
from dotenv import load_dotenv
from courses import COURSES, INSTITUTE_INFO

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_system_prompt():
    courses_text = ""
    for key, course in COURSES.items():
        courses_text += f"""
        Course: {course['name']}
        Duration: {course['duration']}
        Fee: {course['fee']}
        Description: {course['description']}
        Eligibility: {course['eligibility']}
        Mode: {course['mode']}
        Starts: {course['starts']}
        ---"""

    return f"""You are a friendly and helpful admissions counselor for {INSTITUTE_INFO['name']}.
Your tagline is: {INSTITUTE_INFO['tagline']}

You help students with course enquiries on WhatsApp.

Here are the courses you offer:
{courses_text}

Institute Details:
- Email: {INSTITUTE_INFO['contact_email']}
- Phone: {INSTITUTE_INFO['contact_phone']}
- Website: {INSTITUTE_INFO['website']}
- Location: {INSTITUTE_INFO['location']}

Your behavior rules:
1. Always be friendly, warm and encouraging
2. Answer only education and course related questions
3. If a student asks about a course, give full details
4. After answering, always ask if they'd like to enroll or know more
5. When student shows interest in enrolling, ask for their:
   - Full name
   - Email address
   - Phone number
6. Once you have all 3 details, confirm and thank them warmly
7. Keep responses short and WhatsApp friendly
8. Use emojis occasionally to keep it friendly 😊
9. If asked something unrelated, politely redirect to courses
10. Always respond in the same language the student uses
"""

def get_ai_response(conversation_history):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": build_system_prompt()}
        ] + conversation_history,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content