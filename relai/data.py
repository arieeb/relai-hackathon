import pandas as pd
import random
import re
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
        num_conversations = random.randint(3, 20)
        last_message_days_ago = random.randint(1, 45)
        for _ in range(num_conversations):
            convo_date = base_date + timedelta(days=random.randint(0, 90 - last_message_days_ago))
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

def parse_whatsapp(file_content, your_name="You"):
    """Parse WhatsApp exported .txt file into standard dataframe"""
    rows = []
    
    # WhatsApp formats vary by phone/region, handle both
    patterns = [
        r'(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*([AP]M)?\s*[-–]\s*([^:]+):\s*(.+)',
        r'\[(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*([AP]M)?\]\s*([^:]+):\s*(.+)'
    ]
    
    # Detect contact name (most frequent non-"You" sender)
    lines = file_content.split('\n')
    sender_counts = {}
    
    for line in lines:
        for pattern in patterns:
            match = re.match(pattern, line.strip())
            if match:
                groups = match.groups()
                sender = groups[3].strip()
                if sender not in ["You", your_name]:
                    sender_counts[sender] = sender_counts.get(sender, 0) + 1
    
    # The contact is whoever sent the most messages
    contact_name = max(sender_counts, key=sender_counts.get) if sender_counts else "Contact"

    for line in lines:
        for pattern in patterns:
            match = re.match(pattern, line.strip())
            if match:
                groups = match.groups()
                date_str = groups[0]
                time_str = groups[1]
                ampm     = groups[2] or ""
                sender   = groups[3].strip()
                message  = groups[4].strip()

                # Skip system messages
                if any(x in message.lower() for x in [
                    "messages and calls are end-to-end",
                    "created group", "added", "left", "changed",
                    "missed voice call", "missed video call", "<media omitted>"
                ]):
                    continue

                try:
                    time_full = f"{date_str} {time_str} {ampm}".strip()
                    for fmt in [
                        "%m/%d/%Y %I:%M %p", "%d/%m/%Y %I:%M %p",
                        "%m/%d/%y %I:%M %p",  "%d/%m/%y %I:%M %p",
                        "%m/%d/%Y %H:%M",     "%d/%m/%Y %H:%M",
                    ]:
                        try:
                            timestamp = datetime.strptime(time_full, fmt)
                            break
                        except:
                            continue
                    else:
                        continue
                except:
                    continue

                normalized_sender = "You" if sender == your_name else contact_name

                rows.append({
                    "timestamp": timestamp,
                    "contact": contact_name,
                    "sender": normalized_sender,
                    "message": message,
                    "topic": detect_topic(message)
                })
                break

    if not rows:
        return None

    df = pd.DataFrame(rows)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

def detect_topic(message):
    """Simple keyword-based topic detection"""
    message = message.lower()
    if any(w in message for w in ["interview", "placement", "job", "offer", "hr"]):
        return "placement interview"
    elif any(w in message for w in ["exam", "test", "study", "marks", "result"]):
        return "semester exams"
    elif any(w in message for w in ["project", "hackathon", "code", "build"]):
        return "hackathon project"
    elif any(w in message for w in ["movie", "film", "watch", "netflix"]):
        return "movie night"
    elif any(w in message for w in ["cricket", "match", "game", "play", "sport"]):
        return "cricket match"
    elif any(w in message for w in ["plan", "meet", "weekend", "free", "hangout"]):
        return "weekend plans"
    elif any(w in message for w in ["intern", "company", "work", "office"]):
        return "internship offer"
    elif any(w in message for w in ["fest", "event", "college", "campus"]):
        return "college fest"
    elif any(w in message for w in ["assign", "submit", "deadline", "due"]):
        return "assignment deadline"
    else:
        return "general chat"