"""Minimal ticket router using Jev.

Requires: pip install typesafe-sdk
Requires: TYPESAFE_API_KEY env var set.
"""

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient()

TICKETS = [
    "Hi, I've been trying to connect my Stripe account for 3 days and the "
    "integration keeps failing. I'm losing sales. Please help ASAP.",
    "Hey, just wondering what the difference is between the Pro and "
    "Business plans before I upgrade.",
    "You charged me twice this month for the same subscription, this is "
    "unacceptable and I want a refund right now.",
    "The dashboard is showing a blank page after I click 'Export'. Console "
    "shows a 500 error.",
]


def route(ticket: str) -> None:
    response = client.system_one(
        state=ticket,
        questions={
            "department": Choice(
                instructions="Which team should handle this",
                criteria={
                    "billing": "Payment or subscription issues",
                    "technical": "Bugs or integration problems",
                    "sales": "Pricing or account questions",
                },
            ),
            "frustration": Score(
                instructions="How frustrated the customer appears",
                criteria=[
                    "Calm, just stating facts",
                    "Frustrated but civil",
                    "Very angry, strong language",
                ],
            ),
            "is_urgent": Noul(
                instructions="The message conveys urgency or time-sensitivity",
            ),
        },
    )

    dept = response.choices["department"]
    frustration = response.scores["frustration"]
    urgent = response.nouls["is_urgent"]

    print(f"ticket: {ticket[:60]!r}...")
    print(
        f"  -> department={dept.choice} (confidence={dept.confidence:.2f}) "
        f"frustration={frustration.score:.1f} urgent={urgent.noul:.2f}"
    )
    print()


if __name__ == "__main__":
    for ticket in TICKETS:
        route(ticket)
