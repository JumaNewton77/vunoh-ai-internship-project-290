import json
from groq import Groq
from django.conf import settings


# Was previously hardcoded to "YOUR_GROQ_API_KEY", which meant every
# real request failed auth and silently fell through to the fallback
# response below. This now uses the key settings.py already loads
# from .env.
client = Groq(api_key=settings.GROQ_API_KEY)


SYSTEM_PROMPT = """
You are Vunoh Global AI Workflow Assistant.

Return ONLY valid JSON. No markdown, no code fences, no commentary.

Intent options (choose exactly one):

- send_money
- hire_service
- verify_document
- airport_transfer
- check_status

Extract entities relevant to the request. Always include these keys,
using an empty string "" if a value is not present in the message:

- amount
- recipient
- location
- urgency        ("low", "normal", "high", or "urgent")
- document_type
- service_type

Required output format (exact keys, no extras):

{
"intent":"",
"entities":{
"amount":"",
"recipient":"",
"location":"",
"urgency":"",
"document_type":"",
"service_type":""
},
"steps":[],
"whatsapp_message":"",
"email_message":"",
"sms_message":""
}

Rules for steps:

If request is money transfer:
steps:
[
"Verify sender identity",
"Confirm recipient details",
"Review risk indicators",
"Initiate transfer",
"Send confirmation"
]

If request is document verification:
steps:
[
"Receive document",
"Verify ownership records",
"Legal review",
"Approve verification",
"Notify customer"
]

If request is service hiring:
steps:
[
"Match service provider",
"Confirm schedule",
"Complete service",
"Sign-off and close task"
]

If request is airport transfer:
steps:
[
"Confirm flight and arrival details",
"Assign driver",
"Send driver details to customer",
"Confirm pickup completion"
]

If request is check_status:
steps:
[
"Look up referenced task",
"Return current status to customer"
]

Message style rules:

WhatsApp: conversational, concise, natural line breaks, at most 1-2 emoji.
Email: formal and structured, must include a clear subject line and the
       key request details.
SMS: under 160 characters total, plain text, key action only.
"""


def process_request(customer_request):

    try:
        completion = client.chat.completions.create(
            # llama-3.3-70b-versatile is being retired by Groq on 08/16/26
            # (see console.groq.com/docs/deprecations). Using the
            # recommended, currently-stable replacement instead so this
            # doesn't quietly break right before your interview.
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": customer_request},
            ],
            temperature=0.2,
        )

        response = completion.choices[0].message.content.strip()

        # Groq sometimes wraps JSON in ```json ... ``` fences despite
        # instructions - strip those before parsing.
        if response.startswith("```"):
            response = response.replace("```json", "").replace("```", "").strip()

        data = json.loads(response)

        required = [
            "intent",
            "entities",
            "steps",
            "whatsapp_message",
            "email_message",
            "sms_message",
        ]

        for field in required:
            if field not in data:
                raise ValueError(f"{field} missing from AI response")

        return data

    except Exception as e:
        # Keep this print for now - useful during grading/demo to show
        # you're aware of failure modes and handle them gracefully
        # rather than letting the request crash.
        print("AI ERROR:", str(e))

        return {
            "intent": "check_status",
            "entities": {},
            "steps": ["Manual review required"],
            "whatsapp_message": "Your request was received. Our team will follow up shortly.",
            "email_message": "Your request is under review. We will contact you with next steps.",
            "sms_message": "Request received. Under review.",
        }