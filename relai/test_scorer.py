from data import generate_chat_logs
from scorer import compute_bond_scores

def test_scores_generated():
    df = generate_chat_logs()
    scores = compute_bond_scores(df)
    assert len(scores) > 0

def test_bond_score_range():
    df = generate_chat_logs()
    scores = compute_bond_scores(df)
    assert scores["bond_score"].between(0, 100).all()

def test_drift_status_values():
    df = generate_chat_logs()
    scores = compute_bond_scores(df)
    valid = {"🟢 Healthy", "🟡 Fading", "🔴 At Risk"}
    assert set(scores["drift_status"]).issubset(valid)
