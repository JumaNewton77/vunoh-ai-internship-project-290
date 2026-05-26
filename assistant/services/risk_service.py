def calculate_risk(intent, entities):

    risk = 0

    # Safe amount handling
    amount = entities.get(
        "amount",
        0
    )

    try:

        amount = int(
            str(amount).replace(
                "KES",
                ""
            ).replace(
                ",",
                ""
            ).strip()
        )

    except:

        amount = 0


    # Money transfer risk

    if amount > 50000:

        risk += 3

    elif amount > 10000:

        risk += 2


    # Urgency risk

    urgency = entities.get(
        "urgency",
        ""
    )

    if urgency.lower() == "urgent":

        risk += 2


    # Document verification risk

    if intent == "verify_document":

        document = entities.get(
            "document_type",
            ""
        )

        high_risk_keywords = [

            "land",
            "title",
            "title deed",
            "deed",
            "property"
        ]

        if any(

            word in document.lower()

            for word in high_risk_keywords

        ):

            risk += 3


    # Service risk

    if intent == "hire_service":

        risk += 1


    return min(risk,10)