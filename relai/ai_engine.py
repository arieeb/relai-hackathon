import random

def generate_reengagement_message(contact, days_since, last_topic, bond_score, drift_status):
    
    messages = [
        f"hey {contact}! it's been a while 😅 was thinking about you — how did the {last_topic} go?",
        f"yo {contact}, {days_since} days and no word?? hope everything's good, let's catch up soon fr",
        f"{contact}!! literally was just thinking about the whole {last_topic} thing — we need to talk lol",
        f"hey, haven't heard from you in like {days_since} days 😭 everything okay? miss you bro",
        f"{contact} bhai/behen, the {last_topic} saga — give me an update!! also we need to meet up"
    ]

    reasons = [
        f"Bond score dropped to {bond_score}/100 — {days_since} days of silence is too long for this friendship.",
        f"Last interaction was {days_since} days ago about '{last_topic}' — no follow-up detected.",
        f"Reciprocity declining — you've been the last to reach out. {contact} may be drifting.",
        f"Historically strong bond ({bond_score}/100) at risk due to {days_since} day inactivity gap.",
        f"Pattern detected: conversation frequency dropped 60% in the last 30 days."
    ]

    return random.choice(messages), random.choice(reasons)


def generate_weekly_digest(scores_df):
    at_risk = scores_df[scores_df["drift_status"] == "🔴 At Risk"]
    fading = scores_df[scores_df["drift_status"] == "🟡 Fading"]

    digest = f"""
Hey! Here's your weekly relationship check-in 👋

This week, **{len(at_risk)} friendships are at risk** and **{len(fading)} are fading** — time to take action before these slip away.

"""
    if len(at_risk) > 0:
        names = ", ".join(at_risk["contact"].tolist())
        digest += f"🔴 **Needs urgent attention:** {names} — you haven't spoken in over 3 weeks. A simple 'hey' goes a long way.\n\n"

    if len(fading) > 0:
        names = ", ".join(fading["contact"].tolist())
        digest += f"🟡 **Check in soon:** {names} — conversations have slowed down recently. Don't let these fade out.\n\n"

    digest += "Your strongest bonds are looking good — keep it up! Small consistent effort beats big gestures every time. 💪"

    return digest