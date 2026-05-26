import json
from groq import Groq


client = Groq(
    api_key="YOUR_GROQ_API_KEY"
)


SYSTEM_PROMPT = """
You are Vunoh Global AI Workflow Assistant.

Return ONLY valid JSON.

Intent options:

- send_money
- hire_service
- verify_document
- airport_transfer
- check_status

Extract entities:

- amount
- recipient
- location
- urgency
- document_type
- service_type

Required output format:

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

Rules:

If request is money transfer:

steps:
[
"Verify sender",
"Verify recipient",
"Process transfer",
"Send confirmation"
]

If request is document verification:

steps:
[
"Upload document",
"OCR extraction",
"Legal validation",
"Final approval"
]

If request is service hiring:

steps:
[
"Identify provider",
"Schedule service",
"Confirm completion"
]

WhatsApp:
Friendly with emojis.

Email:
Professional and detailed.

SMS:
Maximum 160 characters.
"""

def process_request(customer_request):

    try:

        completion = client.chat.completions.create(

            model="llama3-8b-8192",

            messages=[

                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },

                {
                    "role":"user",
                    "content":customer_request
                }

            ],

            temperature=0.2
        )


        response=(

            completion
            .choices[0]
            .message
            .content
        )


        response=response.strip()


        if response.startswith("```"):

            response=response.replace(
                "```json",
                ""
            )

            response=response.replace(
                "```",
                ""
            )


        data=json.loads(
            response
        )


        required=[

            "intent",
            "entities",
            "steps",
            "whatsapp_message",
            "email_message",
            "sms_message"
        ]


        for field in required:

            if field not in data:

                raise Exception(
                    f"{field} missing"
                )


        return data


    except Exception as e:

        print(
            "AI ERROR:",
            str(e)
        )


        return {

            "intent":"check_status",

            "entities":{},

            "steps":[
                "Manual review required"
            ],

            "whatsapp_message":
            "Your request was received.",

            "email_message":
            "Your request is under review.",

            "sms_message":
            "Request received."
        }