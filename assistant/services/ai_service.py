import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are an AI assistant for Vunoh Global.

Analyze the customer request.

Return ONLY valid JSON.

Example format:

{
    "intent": "verify_document",
    "entities": {
        "location": "Karen",
        "document_type": "title deed"
    },
    "risk_score": 4,
    "employee_assignment": "Legal Verification Officer",
    "steps": [
        "Receive customer request",
        "Verify submitted documents",
        "Contact land registry",
        "Send verification feedback"
    ],
    "whatsapp_message": "Your request has been received.",
    "email_message": "Dear customer, your verification process has started.",
    "sms_message": "Verification request received."
}
"""

def process_request(user_message):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    print("AI RAW RESPONSE:")
    print(content)

    try:
        return json.loads(content)

    except Exception as e:

        print("JSON ERROR:", e)

        return {
            "intent": "check_status",
            "entities": {},
            "risk_score": 1,
            "employee_assignment": "Support Team",
            "steps": [
                "Manual review required"
            ],
            "whatsapp_message": "Your request was received.",
            "email_message": "Your request is under review.",
            "sms_message": "Request received."
        }
    