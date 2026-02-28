import random
from transformers import pipeline

# Load sentiment model once (cached in memory)
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(messages):
    if not messages:
        return "NEUTRAL", 0.5

    # Use last 20 messages for recent emotional context
    recent_text = " ".join(messages[-20:])

    result = sentiment_model(recent_text[:512])[0]
    label = result["label"]
    confidence = round(result["score"] * 100, 1)

    return label, confidence


def generate_reengagement_message(contact, days_since, last_topic, bond_score, drift_status, messages=None):

    sentiment_label, confidence = analyze_sentiment(messages)

    # Tone selection based on sentiment
    if sentiment_label == "NEGATIVE":
        messages_pool = [
            f"hey {contact}, just wanted to check in. hope everything's okay on your end ❤️",
            f"haven't heard from you in {days_since} days — if anything’s been stressful, I’m here.",
            f"thinking about you. how are things going lately?"
        ]
        reason = f"Sentiment detected as NEGATIVE ({confidence}% confidence). Suggesting a supportive tone."

    elif sentiment_label == "POSITIVE":
        messages_pool = [
            f"yo {contact}! it’s been {days_since} days — we need another fun convo like the {last_topic} one 😄",
            f"hey superstar, how did the {last_topic} go?? update me!",
            f"bro we’ve been too quiet lately. let’s fix that 🔥"
        ]
        reason = f"Sentiment detected as POSITIVE ({confidence}% confidence). Suggesting energetic tone."

    else:
        messages_pool = [
            f"hey {contact}! long time no talk — how’s everything?",
            f"{days_since} days already?? let’s catch up soon.",
            f"what’s new with you these days?"
        ]
        reason = f"Sentiment detected as NEUTRAL ({confidence}% confidence). Using balanced tone."

    return random.choice(messages_pool), reason


def generate_weekly_digest(scores_df):
    at_risk = scores_df[scores_df["drift_status"] == "🔴 At Risk"]
    fading = scores_df[scores_df["drift_status"] == "🟡 Fading"]

    digest = f"""
Hey! Here's your weekly relationship check-in 👋

This week, {len(at_risk)} friendships are at risk and {len(fading)} are fading.

"""

    if len(at_risk) > 0:
        names = ", ".join(at_risk["contact"].tolist())
        digest += f"🔴 Needs urgent attention: {names}\n\n"

    if len(fading) > 0:
        names = ", ".join(fading["contact"].tolist())
        digest += f"🟡 Check in soon: {names}\n\n"

    digest += "Strong bonds are holding steady — keep the consistency going 💪"

    return digest