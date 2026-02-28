import pandas as pd
import random
from datetime import datetime, timedelta

contacts = [
    "Riya", "Arjun", "Sneha", "Kabir", "Priya", "Dev", "Ananya"
]

topics = [
    "placement interview", "hackathon project", "semester exams",
    "college fest", "internship offer", "assignment deadline",
    "weekend plans", "movie night", "cricket match", "startup idea"
]

messages_pool = [
    "hey what's up", "did you finish the assignment?", "let's catch up soon",
    "bro when are you free", "miss hanging out with you",
    "all the best for your interview!", "how did it go?",
    "we should plan something this weekend", "you free tomorrow?",
    "haven't talked in a while", "check this out", "lmk when you're free",
    "good luck with everything", "how's the internship going?",
    "we need to meet up fr", "called you, you didn't pick up",
    "ping me when you're done", "are you coming to the fest?"
]

def generate_chat_logs():
    rows = []
    base_date = datetime.now() - timedelta(days=90)

    for contact in contacts:
        # each contact gets different interaction pattern
        num_conversations = random.randint(3, 20)
        last_message_days_ago = random.randint(1, 45)

        for _ in range(num_conversations):
            convo_date = base_date + timedelta(
                days=random.randint(0, 90 - last_message_days_ago)
            )
            num_messages = random.randint(2, 8)
            topic = random.choice(topics)

            for m in range(num_messages):
                sender = random.choice(["You", contact])
                message = random.choice(messages_pool)
                timestamp = convo_date + timedelta(minutes=m * random.randint(1, 15))
                rows.append({
                    "timestamp": timestamp,
                    "contact": contact,
                    "sender": sender,
                    "message": message,
                    "topic": topic
                })

    df = pd.DataFrame(rows)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = generate_chat_logs()
    print(df.head(20))
    print(f"\nTotal messages: {len(df)}")
    print(f"Contacts: {df['contact'].unique()}")