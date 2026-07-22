"""
Risk scoring for Vunoh diaspora requests.

Score is 0-100 (matches the bands documented in the README):
    0-30   Low
    31-60  Medium
    61-100 High

Design notes (for the "Decisions I made and why" README section):
- Previously the score was capped at min(risk, 10) with no documented
  bands actually matching that cap - this rewrite makes the code match
  the documented 0-100 scale.
- Urgency previously only matched the literal string "urgent", but the
  AI's own example output in the README uses "high" - that meant the
  urgency factor silently never fired for the AI's typical output.
  Both "high" and "urgent" now count.
- The brief explicitly calls out two factors that were missing:
  unverified/unknown recipients, and reduced risk for a returning
  customer with a clean history. Both are added below.
"""


def _parse_amount(raw_amount):
    """Best-effort parse of an amount string like 'KES 15,000' -> 15000."""
    try:
        cleaned = (
            str(raw_amount)
            .upper()
            .replace("KES", "")
            .replace(",", "")
            .strip()
        )
        return int(float(cleaned)) if cleaned else 0
    except (ValueError, TypeError):
        return 0


def calculate_risk(intent, entities, is_returning_customer=False):
    """
    intent: one of the Task.INTENT_CHOICES values
    entities: dict extracted by the AI (amount, recipient, location,
              urgency, document_type, service_type)
    is_returning_customer: True if this user has at least one prior
              task with no flagged issues - pass this in from the view,
              e.g. `Task.objects.filter(user=request.user).exists()`
    """
    entities = entities or {}
    risk = 0
    reasons = []

    amount = _parse_amount(entities.get("amount", 0))
    urgency = str(entities.get("urgency", "")).lower()
    is_urgent = urgency in ("high", "urgent")

    # --- Money transfer amount ---
    if intent == "send_money":
        if amount > 100000:
            risk += 35
            reasons.append("Large transfer amount (> KES 100,000)")
        elif amount > 50000:
            risk += 20
            reasons.append("Moderate-large transfer amount")
        elif amount > 10000:
            risk += 10
            reasons.append("Above-average transfer amount")

        # Unknown / unverified recipient - the AI extracts a recipient
        # label (e.g. "mother") but we have no record confirming that
        # name is a previously-verified beneficiary on this account.
        recipient = str(entities.get("recipient", "")).strip()
        if not recipient:
            risk += 20
            reasons.append("No recipient identified")
        elif recipient.lower() in ("unknown", "someone", "a friend"):
            risk += 20
            reasons.append("Unverified/unclear recipient")

    # --- Urgency (compounds with amount, per the brief's example) ---
    if is_urgent:
        risk += 15
        reasons.append("Urgent request")
        if intent == "send_money" and amount > 100000:
            risk += 10
            reasons.append("High urgency combined with large amount")

    # --- Document verification ---
    if intent == "verify_document":
        document_type = str(entities.get("document_type", "")).lower()
        high_risk_keywords = ("land", "title", "title deed", "deed", "property")
        if any(word in document_type for word in high_risk_keywords):
            risk += 25
            reasons.append("Land title / property document verification")
        else:
            risk += 10
            reasons.append("General document verification")

    # --- Service hire (lowest baseline risk category) ---
    if intent == "hire_service":
        risk += 5
        reasons.append("Routine service request")

    # --- Airport transfer: time-sensitive, involves a third-party driver ---
    if intent == "airport_transfer":
        risk += 10
        reasons.append("Time-sensitive logistics request")

    # --- Returning customer discount ---
    if is_returning_customer:
        risk -= 10
        reasons.append("Returning customer with prior history")

    risk = max(0, min(risk, 100))

    if risk <= 30:
        level = "Low"
    elif risk <= 60:
        level = "Medium"
    else:
        level = "High"

    return {
        "score": risk,
        "level": level,
        "reasons": reasons,
    }