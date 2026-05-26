def assign_employee(intent):

    assignments={

        "send_money":"Finance Team",

        "hire_service":"Operations Team",

        "verify_document":"Legal Team",

        "airport_transfer":"Transport Team",

        "check_status":"Support Team"

    }

    return assignments.get(
        intent,
        "General Support"
    )