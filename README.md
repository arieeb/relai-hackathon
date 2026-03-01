🧠 RelAI — Relationship Intelligence on Autopilot

AI-powered relationship analysis and automation system built for Paradigm 1.0 — CodeBase, MPSTME.

🚀 Problem

Gen Z is always connected — but meaningful conversations still fade.

Between academics, internships, side projects, and social life, important relationships suffer due to:

Delayed replies

Forgotten follow-ups

Missed important mentions

Buried plans

Long inactivity gaps

The issue is not communication access — it’s the lack of intelligent automation around it.

RelAI solves this by analyzing communication patterns and proactively suggesting meaningful social actions before relationships weaken.

🧠 What RelAI Does

RelAI transforms raw chat logs into structured insights and automated relationship actions.

Core Features

Communication behavior analysis over time

Multi-factor bond score calculation

Drift detection (relationship weakening detection)

Sentiment analysis using DistilBERT (runs locally)

Smart re-engagement message suggestions

Mood-aware reply assistant (Match Emotion / Lift Mood)

Weekly relationship summary

WhatsApp chat export (.txt) support

🏗️ Architecture

Chat Logs (.txt or synthetic data)
→ Parsing & Normalization (data.py)
→ Scoring Engine (scorer.py)
→ Sentiment Analysis (DistilBERT, local model)
→ Decision Engine (ai_engine.py)
→ Automation Outputs
→ Streamlit Dashboard (app.py)

📊 Bond Score Formula

Bond Score (0–100) =

0.30 × Recency

0.25 × Frequency

0.25 × Depth

0.20 × Reciprocity

Drift Velocity

Measures week-over-week change in bond score.

Used to classify relationships as:

🔴 At Risk

🟡 Fading

🟢 Healthy

⚪ Stable

🤖 AI Components
Sentiment Analysis

Model used:
distilbert-base-uncased-finetuned-sst-2-english

Runs fully offline

No API cost

Detects positive / negative tone

Provides confidence score

Smart Re-Engagement Engine

Generates contextual suggestions based on:

Drift velocity

Sentiment trend

Last topic discussed

Days since last interaction

Smart Reply Assistant

User chooses:

Match Emotion

Lift Mood

Replies are generated using:

Sentiment detection

Conversation context

Human-style response templates

Designed to feel natural, not robotic.

📱 WhatsApp Integration

Export chat:

Android
Open chat → 3 dots → More → Export Chat → Without Media

iPhone
Open chat → Contact → Export Chat → Without Media

Upload the .txt file into the dashboard.

RelAI automatically:

Parses timestamps

Identifies participants

Detects topics

Runs full analysis

🖥️ Tech Stack

Python

Streamlit

Pandas

PyVis

HuggingFace Transformers

DistilBERT

🧪 How to Run

Install dependencies:

pip install streamlit pandas pyvis transformers torch

Run the app:

streamlit run app.py

🎯 Why This Project Stands Out

Structured automation pipeline (not just a chatbot)

Behavioral modeling over time

Explainable scoring mechanism

Drift velocity innovation

Modular system design

Local ML integration

Real-world usability

🔮 Future Improvements

Multi-contact bulk analysis

Conversation theme classification

Top word frequency analytics

Emotional trend visualization

Reminder integration

Adaptive learning from feedback

👤 Author

Arieeb Ali
Paradigm 1.0 Hackathon
