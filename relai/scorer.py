import pandas as pd
from datetime import datetime, timedelta

def compute_bond_scores(df):
    now = datetime.now()
    scores = []

    for contact, group in df.groupby("contact"):

        def score_for_period(g):
            if len(g) == 0:
                return 0, 0, 0, 0

            last_msg_time = g["timestamp"].max()
            days_since = (now - last_msg_time).days
            if days_since <= 3: recency = 100
            elif days_since <= 7: recency = 80
            elif days_since <= 14: recency = 60
            elif days_since <= 30: recency = 35
            else: recency = 10

            total_messages = len(g)
            if total_messages >= 50: frequency = 100
            elif total_messages >= 30: frequency = 75
            elif total_messages >= 15: frequency = 50
            elif total_messages >= 5: frequency = 25
            else: frequency = 10

            unique_topics = g["topic"].nunique()
            depth = min(unique_topics * 10, 100)

            you_msgs = len(g[g["sender"] == "You"])
            them_msgs = len(g[g["sender"] == contact])
            total = you_msgs + them_msgs
            if total == 0: reciprocity = 0
            else:
                ratio = min(you_msgs, them_msgs) / max(you_msgs, them_msgs)
                reciprocity = ratio * 100

            bond = (0.30 * recency + 0.25 * frequency + 0.25 * depth + 0.20 * reciprocity)
            return round(bond, 1), round(recency, 1), round(frequency, 1), round(depth, 1), round(reciprocity, 1)

        # Current bond score
        result = score_for_period(group)
        bond, recency, frequency, depth, reciprocity = result

        # Previous week bond score (messages older than 7 days)
        cutoff = now - timedelta(days=7)
        older = group[group["timestamp"] < cutoff]
        if len(older) > 0:
            old_result = score_for_period(older)
            old_bond = old_result[0]
        else:
            old_bond = bond

        drift_velocity = round(bond - old_bond, 1)

        # Drift status
        if drift_velocity <= -5:
            drift_label = f"🔴 -{abs(drift_velocity)} pts/week"
        elif drift_velocity < 0:
            drift_label = f"🟡 -{abs(drift_velocity)} pts/week"
        elif drift_velocity > 0:
            drift_label = f"🟢 +{drift_velocity} pts/week"
        else:
            drift_label = "⚪ Stable"

        last_msg_time = group["timestamp"].max()
        days_since = (now - last_msg_time).days

        drift_status = "🔴 At Risk" if days_since > 20 and bond < 50 else \
                       "🟡 Fading"  if days_since > 10 and bond < 65 else \
                       "🟢 Healthy"

        scores.append({
            "contact": contact,
            "bond_score": bond,
            "recency_score": recency,
            "frequency_score": frequency,
            "depth_score": depth,
            "reciprocity_score": reciprocity,
            "drift_velocity": drift_velocity,
            "drift_label": drift_label,
            "days_since_contact": days_since,
            "total_messages": len(group),
            "drift_status": drift_status,
            "last_topic": group["topic"].iloc[-1]
        })

    result = pd.DataFrame(scores)
    result = result.sort_values("bond_score", ascending=False).reset_index(drop=True)
    return result

if __name__ == "__main__":
    from data import generate_chat_logs
    df = generate_chat_logs()
    scores = compute_bond_scores(df)
    print(scores[["contact", "bond_score", "drift_velocity", "drift_label", "drift_status"]])