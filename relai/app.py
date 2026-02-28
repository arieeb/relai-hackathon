import streamlit as st
import pandas as pd
from data import generate_chat_logs, parse_whatsapp
from scorer import compute_bond_scores
from ai_engine import generate_reengagement_message, generate_weekly_digest
from pyvis.network import Network
from personality import compute_personality_profile, extract_top_terms
import streamlit.components.v1 as components
import tempfile
import os


st.set_page_config(page_title="RelAI", page_icon="🧠", layout="wide")

# =========================
# LOAD DATA
# =========================

@st.cache_data
def load_demo():
    return generate_chat_logs()

uploaded_file = st.file_uploader("📱 Upload WhatsApp Chat (.txt)", type=["txt"])
your_name = st.text_input("Your Name in Chat", value="You")

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    parsed = parse_whatsapp(content, your_name)
    if parsed is not None:
        df = parsed
        st.success(f"Live data loaded — {len(df)} messages")
    else:
        df = load_demo()
        st.warning("Could not parse file — using demo data")
else:
    df = load_demo()
    st.info("Using synthetic demo data")

# =========================
# COMPUTE SCORES
# =========================

scores = compute_bond_scores(df)

total   = len(scores)
healthy = len(scores[scores["drift_status"] == "🟢 Healthy"])
fading  = len(scores[scores["drift_status"] == "🟡 Fading"])
at_risk = len(scores[scores["drift_status"] == "🔴 At Risk"])

st.title("🧠 RelAI — Relationship Intelligence Dashboard")

# =========================
# METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Contacts", total)
col2.metric("Healthy", healthy)
col3.metric("Fading", fading)
col4.metric("At Risk", at_risk)

# =========================
# NETWORK GRAPH
# =========================

st.subheader("🕸️ Network Overview")

net = Network(height="400px", width="100%", bgcolor="#ffffff")

net.add_node("You", color="#5b6ef5", size=30)

for _, row in scores.iterrows():
    color = "#ef4444" if row["drift_status"] == "🔴 At Risk" else \
            "#f59e0b" if row["drift_status"] == "🟡 Fading" else "#00c06a"

    net.add_node(
        row["contact"],
        color=color,
        size=max(12, int(row["bond_score"]/4)),
        title=f"Bond: {row['bond_score']} | {row['drift_status']}"
    )

    net.add_edge("You", row["contact"], width=row["bond_score"]/25)

with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
    net.save_graph(tmp.name)
    html = open(tmp.name).read()
    components.html(html, height=420)
    os.unlink(tmp.name)

# =========================
# CONTACT LIST
# =========================

st.subheader("🎯 Contacts")

st.dataframe(scores[[
    "contact",
    "bond_score",
    "drift_status",
    "drift_velocity",
    "days_since_contact"
]])

# =========================
# AI MESSAGE SUGGESTION
# =========================

st.subheader("✨ AI Re-engagement Suggestion")

not_healthy = scores[scores["drift_status"] != "🟢 Healthy"]
if len(not_healthy) == 0:
    not_healthy = scores

selected = st.selectbox("Select Contact", not_healthy["contact"].tolist())

sel_row = scores[scores["contact"] == selected].iloc[0]

if st.button("Generate AI Message"):

    # 🔥 THIS IS THE IMPORTANT PART
    contact_msgs = df[df["contact"] == selected]["message"].tolist()

    msg, reason = generate_reengagement_message(
        sel_row["contact"],
        sel_row["days_since_contact"],
        sel_row["last_topic"],
        sel_row["bond_score"],
        sel_row["drift_status"],
        messages=contact_msgs  # <-- Passing real chat history
    )

    st.markdown("### 🔍 Reason")
    st.info(reason)

    st.markdown("### 💬 Suggested Message")
    st.success(msg)





st.subheader("🧠 Your Communication Personality")

profile = compute_personality_profile(df)

if profile:
    for theme, percent in profile.items():
        st.write(f"{theme}: {percent}%")
else:
    st.write("Not enough data.")

st.subheader("🔥 Top 5 Words You Use")

top_terms = extract_top_terms(df)

for word, count in top_terms:
    st.write(f"{word} ({count} times)")




    
# =========================
# WEEKLY DIGEST
# =========================

st.subheader("📋 Weekly Network Summary")

if st.button("Generate Weekly Digest"):
    digest = generate_weekly_digest(scores)
    st.write(digest)

st.caption("© 2026 RelAI · Built for Paradigm 1.0")