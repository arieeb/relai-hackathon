import re
from collections import Counter

LOVE = ["love", "miss", "baby", "cute", "heart", "hug"]
CASUAL = ["bro", "lol", "haha", "yo", "sup", "what's up"]
GOSSIP = ["heard", "did you see", "she said", "he said"]
ACADEMIC = ["exam", "assignment", "project", "study", "marks"]
WORK = ["office", "meeting", "intern", "company", "work"]

STOPWORDS = set([
    "hi", "hello", "bye", "miss", "you", "the", "is", "are",
    "and", "to", "of", "a", "in", "on", "for", "lol", "haha"
])

def classify_message_theme(message):
    message = message.lower()

    scores = {
        "Romantic": sum(word in message for word in LOVE),
        "Casual": sum(word in message for word in CASUAL),
        "Gossip": sum(word in message for word in GOSSIP),
        "Academic": sum(word in message for word in ACADEMIC),
        "Work": sum(word in message for word in WORK)
    }

    return max(scores, key=scores.get)


def compute_personality_profile(df):
    you_df = df[df["sender"] == "You"]

    theme_counts = Counter()

    for msg in you_df["message"]:
        theme = classify_message_theme(msg)
        theme_counts[theme] += 1

    total = sum(theme_counts.values())

    if total == 0:
        return {}

    profile = {
        theme: round((count / total) * 100, 1)
        for theme, count in theme_counts.items()
    }

    return profile


def extract_top_terms(df):
    you_df = df[df["sender"] == "You"]

    words = []

    for message in you_df["message"]:
        tokens = re.findall(r'\b[a-zA-Z]{3,}\b', message.lower())
        words.extend([w for w in tokens if w not in STOPWORDS])

    counter = Counter(words)
    return counter.most_common(5)