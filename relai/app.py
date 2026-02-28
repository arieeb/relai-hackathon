import streamlit as st
import pandas as pd
from data import generate_chat_logs
from scorer import compute_bond_scores
from ai_engine import generate_reengagement_message, generate_weekly_digest
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="RelAI", page_icon="🧠", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { font-family: 'DM Sans', sans-serif; background: #f0f2f8; color: #0f0f1a; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }
.navbar {
    background: #fff; padding: 0 2rem; height: 64px;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid #e8eaf0; position: sticky; top: 0; z-index: 100;
}
.nav-left { display: flex; align-items: center; gap: 10px; }
.nav-logo {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #5b6ef5, #8b5cf6);
    border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
}
.nav-name { font-size: 1.2rem; font-weight: 700; color: #0f0f1a; }
.nav-tag { font-size: 0.82rem; color: #9999bb; }
.page { padding: 1.8rem 2rem; }
.metrics { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.6rem; }
.mcard {
    background: #fff; border-radius: 14px; padding: 1.2rem 1.4rem;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.mcard-left .num { font-size: 2rem; font-weight: 800; line-height: 1; }
.mcard-left .lbl { font-size: 0.78rem; color: #9999bb; text-transform: uppercase; letter-spacing: .6px; margin-top: 4px; font-weight: 500; }
.mcard-icon { width: 44px; height: 44px; border-radius: 11px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
.ic-blue{background:#eef0ff} .ic-green{background:#e6f9f0} .ic-orange{background:#fff4e5} .ic-red{background:#fff0f0}
.c-blue{color:#5b6ef5} .c-green{color:#00c06a} .c-orange{color:#f59e0b} .c-red{color:#ef4444}
.two-col { display: grid; grid-template-columns: 1.3fr 1fr; gap: 1.2rem; margin-bottom: 1.2rem; }
.card { background: #fff; border-radius: 14px; padding: 1.3rem 1.4rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-bottom: 1.2rem; }
.card-title { font-size: 0.95rem; font-weight: 700; color: #0f0f1a; margin-bottom: 1rem; display: flex; align-items: center; gap: 6px; }
.citem { padding: 0.85rem 0; border-bottom: 1px solid #f2f2f8; }
.citem:last-child { border-bottom: none; padding-bottom: 0; }
.citem-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 3px; }
.cname { font-weight: 600; font-size: 0.92rem; display: flex; align-items: center; gap: 7px; }
.cdot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }
.dg{background:#00c06a} .dy{background:#f59e0b} .dr{background:#ef4444}
.cdays { font-size: 0.78rem; color: #b0b0cc; font-weight: 500; }
.ctopic { font-size: 0.78rem; color: #b0b0cc; margin-bottom: 4px; }
.drift-tag { display: inline-block; font-size: 0.72rem; font-weight: 600; padding: 2px 8px; border-radius: 20px; margin-bottom: 6px; }
.drift-red{background:#fff0f0;color:#ef4444} .drift-yellow{background:#fff8e6;color:#f59e0b}
.drift-green{background:#e6f9f0;color:#00c06a} .drift-grey{background:#f4f4f8;color:#9999bb}
.brow { display: flex; align-items: center; gap: 8px; }
.blbl { font-size: 0.72rem; color: #c0c0d8; white-space: nowrap; }
.btrack { flex: 1; height: 5px; background: #f0f0f8; border-radius: 3px; overflow: hidden; }
.bfill { height: 100%; border-radius: 3px; }
.bpct { font-size: 0.72rem; color: #b0b0cc; font-weight: 600; white-space: nowrap; }
.pitem {
    display: flex; align-items: flex-start; gap: 1rem;
    padding: 1rem; border-radius: 12px; margin-bottom: 0.7rem;
    border: 1px solid #f0f0f8;
}
.pitem-red{background:#fff8f8;border-color:#ffd8d8} .pitem-yellow{background:#fffbf0;border-color:#ffe8b0}
.prank { font-size: 1.1rem; font-weight: 800; color: #c0c0d8; width: 24px; flex-shrink: 0; }
.pname { font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; }
.pdetail { font-size: 0.78rem; color: #8888aa; line-height: 1.7; }
.pbadge { margin-left: auto; font-size: 0.72rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; white-space: nowrap; align-self: flex-start; }
.badge-red{background:#ef4444;color:#fff} .badge-yellow{background:#f59e0b;color:#fff}
.breakdown { background: #f7f6ff; border: 1px solid #ddd8ff; border-radius: 12px; padding: 1rem 1.2rem; margin-top: 0.8rem; }
.breakdown-title { font-size: 0.82rem; font-weight: 700; color: #5b4fcf; margin-bottom: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; }
.bkrow { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.bklbl { font-size: 0.82rem; color: #555577; width: 100px; flex-shrink: 0; }
.bktrack { flex: 1; height: 7px; background: #e8e4ff; border-radius: 4px; overflow: hidden; }
.bkfill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #5b6ef5, #8b5cf6); }
.bkval { font-size: 0.82rem; font-weight: 700; color: #5b4fcf; width: 50px; text-align: right; }
.bktotal { font-size: 0.92rem; font-weight: 800; color: #0f0f1a; margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #ddd8ff; }
.ai-output { background: #f7f6ff; border: 1px solid #ddd8ff; border-radius: 12px; padding: 1rem 1.1rem; margin-top: 0.8rem; }
.ai-reason { font-size: 0.78rem; color: #6c4fcf; background: #ece8ff; border-radius: 7px; padding: 4px 10px; margin-bottom: 8px; display: inline-block; font-weight: 500; }
.ai-msg { font-size: 0.95rem; color: #0f0f1a; font-weight: 500; line-height: 1.6; }
.digest-out { background: #f7f6ff; border: 1px solid #ddd8ff; border-radius: 12px; padding: 1rem 1.2rem; margin-top: 0.8rem; font-size: 0.9rem; color: #2a2a4a; line-height: 1.8; }
.stButton > button {
    background: linear-gradient(135deg, #5b6ef5, #8b5cf6) !important;
    color: #fff !important; border: none !important; border-radius: 9px !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    padding: 0.5rem 1.2rem !important; width: 100% !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-testid="stSelectbox"] > div > div { border-radius: 9px !important; border: 1.5px solid #e4e4f0 !important; }
div[data-testid="stSelectbox"] label { display: none !important; }
.footer { text-align: center; padding: 1.5rem 0 0.5rem; color: #c0c0d8; font-size: 0.78rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = generate_chat_logs()
    scores = compute_bond_scores(df)
    return df, scores

df, scores = load_data()

total   = len(scores)
healthy = len(scores[scores["drift_status"] == "🟢 Healthy"])
fading  = len(scores[scores["drift_status"] == "🟡 Fading"])
at_risk = len(scores[scores["drift_status"] == "🔴 At Risk"])

# NAVBAR
st.markdown("""
<div class="navbar">
  <div class="nav-left">
    <div class="nav-logo">🧠</div>
    <span class="nav-name">RelAI</span>
  </div>
  <span class="nav-tag">AI-Powered Relationship Intelligence</span>
</div>
<div class="page">
""", unsafe_allow_html=True)

# METRICS
st.markdown(f"""
<div class="metrics">
  <div class="mcard"><div class="mcard-left"><div class="num c-blue">{total}</div><div class="lbl">Total Contacts</div></div><div class="mcard-icon ic-blue">👥</div></div>
  <div class="mcard"><div class="mcard-left"><div class="num c-green">{healthy}</div><div class="lbl">Healthy</div></div><div class="mcard-icon ic-green">💚</div></div>
  <div class="mcard"><div class="mcard-left"><div class="num c-orange">{fading}</div><div class="lbl">Fading</div></div><div class="mcard-icon ic-orange">📉</div></div>
  <div class="mcard"><div class="mcard-left"><div class="num c-red">{at_risk}</div><div class="lbl">At Risk</div></div><div class="mcard-icon ic-red">⚠️</div></div>
</div>
""", unsafe_allow_html=True)

# TWO COL
st.markdown('<div class="two-col">', unsafe_allow_html=True)

# LEFT - graph
st.markdown('<div class="card"><div class="card-title">🕸️ Network Overview</div>', unsafe_allow_html=True)
net = Network(height="370px", width="100%", bgcolor="#ffffff", font_color="#0f0f1a")
net.add_node("You", color="#5b6ef5", size=32, title="You", shape="dot")
for _, row in scores.iterrows():
    color = "#ef4444" if row["drift_status"] == "🔴 At Risk" else \
            "#f59e0b" if row["drift_status"] == "🟡 Fading" else "#00c06a"
    net.add_node(row["contact"], color=color, size=max(12, int(row["bond_score"]/4)),
                 title=row["contact"] + "\nBond: " + str(row["bond_score"]) + "/100\n" + row["drift_status"] + "\nDrift: " + row["drift_label"])
    net.add_edge("You", row["contact"], width=row["bond_score"]/28, color="#e4e4f0")
net.set_options('{"physics":{"forceAtlas2Based":{"gravitationalConstant":-50,"springLength":100},"solver":"forceAtlas2Based"}}')
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
    net.save_graph(tmp.name)
    html = open(tmp.name).read()
    components.html(html, height=390)
    os.unlink(tmp.name)
st.markdown('</div>', unsafe_allow_html=True)

# RIGHT - contacts
st.markdown('<div class="card"><div class="card-title">🎯 Your Contacts</div>', unsafe_allow_html=True)
for _, row in scores.iterrows():
    dot = "dr" if row["drift_status"] == "🔴 At Risk" else "dy" if row["drift_status"] == "🟡 Fading" else "dg"
    bar = "#ef4444" if row["drift_status"] == "🔴 At Risk" else "#f59e0b" if row["drift_status"] == "🟡 Fading" else "#00c06a"
    bond = int(row["bond_score"])
    dv = row["drift_velocity"]
    if dv <= -5:   dtag, dcls = row["drift_label"], "drift-red"
    elif dv < 0:   dtag, dcls = row["drift_label"], "drift-yellow"
    elif dv > 0:   dtag, dcls = row["drift_label"], "drift-green"
    else:          dtag, dcls = "Stable", "drift-grey"
    html_block = '<div class="citem">'
    html_block += '<div class="citem-top">'
    html_block += '<div class="cname"><span class="cdot ' + dot + '"></span>' + row["contact"] + '</div>'
    html_block += '<div class="cdays">' + str(row["days_since_contact"]) + 'd ago</div>'
    html_block += '</div>'
    html_block += '<div class="ctopic">Last: ' + row["last_topic"] + '</div>'
    html_block += '<span class="drift-tag ' + dcls + '">' + dtag + '</span>'
    html_block += '<div class="brow">'
    html_block += '<div class="blbl">Bond Strength</div>'
    html_block += '<div class="btrack"><div class="bfill" style="width:' + str(bond) + '%;background:' + bar + '"></div></div>'
    html_block += '<div class="bpct">' + str(bond) + '%</div>'
    html_block += '</div></div>'
    st.markdown(html_block, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# PRIORITY FEED
st.markdown('<div class="card"><div class="card-title">🚨 Priority Feed — Needs Attention</div>', unsafe_allow_html=True)
priority = scores[scores["drift_status"] != "🟢 Healthy"].sort_values("bond_score").head(5)
if len(priority) == 0:
    st.markdown('<p style="color:#9999bb;font-size:0.9rem">All relationships are healthy! 🎉</p>', unsafe_allow_html=True)
else:
    for i, (_, row) in enumerate(priority.iterrows()):
        is_red = row["drift_status"] == "🔴 At Risk"
        pcls   = "pitem-red" if is_red else "pitem-yellow"
        bcls   = "badge-red" if is_red else "badge-yellow"
        label  = "Urgent" if is_red else "Fading"
        dv     = row["drift_velocity"]
        drift_str = "Drift: " + ("+" if dv > 0 else "") + str(round(dv, 1)) + " pts/week"
        html_block = '<div class="pitem ' + pcls + '">'
        html_block += '<div class="prank">' + str(i+1) + '</div>'
        html_block += '<div><div class="pname">' + row["contact"] + '</div>'
        html_block += '<div class="pdetail">No conversation in ' + str(row["days_since_contact"]) + ' days<br>'
        html_block += 'Last topic: ' + row["last_topic"] + '<br>' + drift_str + '</div></div>'
        html_block += '<div class="pbadge ' + bcls + '">' + label + '</div>'
        html_block += '</div>'
        st.markdown(html_block, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# AI MESSAGE + BREAKDOWN
st.markdown('<div class="card"><div class="card-title">✨ AI Message Suggestion</div>', unsafe_allow_html=True)
not_healthy = scores[scores["drift_status"] != "🟢 Healthy"]
col_a, col_b = st.columns([4, 1])
with col_a:
    selected = st.selectbox("contact", not_healthy["contact"].tolist(), label_visibility="collapsed")
with col_b:
    gen = st.button("Generate")

sel_row = scores[scores["contact"] == selected].iloc[0]
r  = sel_row["recency_score"]
fr = sel_row["frequency_score"]
d  = sel_row["depth_score"]
rc = sel_row["reciprocity_score"]
tot = sel_row["bond_score"]

bk  = '<div class="breakdown"><div class="breakdown-title">Bond Score Breakdown</div>'
bk += '<div class="bkrow"><div class="bklbl">Recency</div><div class="bktrack"><div class="bkfill" style="width:' + str(r) + '%"></div></div><div class="bkval">' + str(r) + '/100</div></div>'
bk += '<div class="bkrow"><div class="bklbl">Frequency</div><div class="bktrack"><div class="bkfill" style="width:' + str(fr) + '%"></div></div><div class="bkval">' + str(fr) + '/100</div></div>'
bk += '<div class="bkrow"><div class="bklbl">Depth</div><div class="bktrack"><div class="bkfill" style="width:' + str(d) + '%"></div></div><div class="bkval">' + str(d) + '/100</div></div>'
bk += '<div class="bkrow"><div class="bklbl">Reciprocity</div><div class="bktrack"><div class="bkfill" style="width:' + str(rc) + '%"></div></div><div class="bkval">' + str(rc) + '/100</div></div>'
bk += '<div class="bktotal">Total Bond Score: ' + str(tot) + ' / 100</div></div>'
st.markdown(bk, unsafe_allow_html=True)

if gen:
    msg, reason = generate_reengagement_message(
        sel_row["contact"], sel_row["days_since_contact"],
        sel_row["last_topic"], sel_row["bond_score"], sel_row["drift_status"]
    )
    ai  = '<div class="ai-output">'
    ai += '<div class="ai-reason">🔍 ' + reason + '</div>'
    ai += '<div class="ai-msg">' + msg + '</div>'
    ai += '</div>'
    st.markdown(ai, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# WEEKLY DIGEST
st.markdown('<div class="card"><div class="card-title">📋 Weekly Network Summary</div>', unsafe_allow_html=True)
if st.button("Generate Summary"):
    digest = generate_weekly_digest(scores)
    st.markdown('<div class="digest-out">' + digest + '</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">© 2026 RelAI · Built for Paradigm 1.0, CodeBase MPSTME</div></div>', unsafe_allow_html=True)
