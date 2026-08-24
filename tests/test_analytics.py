import json
import io
import sys
from src.analytics import log_analysis_started, log_analysis_completed, log_analysis_failed, log_feedback_submitted

def test_analytics_started(capsys):
    log_analysis_started()
    captured = capsys.readouterr()
    data = json.loads(captured.out.strip())
    assert data["event"] == "analysis_started"
    assert "timestamp" in data
    # No PII
    assert "resume" not in data
    assert "jd" not in data

def test_analytics_completed(capsys):
    log_analysis_completed(
        duration_ms=150,
        resume_page_count=2,
        recommendation_count=3,
        high_impact_count=1,
        medium_impact_count=2
    )
    captured = capsys.readouterr()
    data = json.loads(captured.out.strip())
    assert data["event"] == "analysis_completed"
    assert data["analysis_duration_ms"] == 150
    assert data["resume_page_count"] == 2
    assert data["recommendation_count"] == 3
    assert data["high_impact_count"] == 1
    assert data["medium_impact_count"] == 2
    # No PII
    assert "resume" not in data
    assert "jd" not in data

def test_analytics_failed(capsys):
    log_analysis_failed("parsing")
    captured = capsys.readouterr()
    data = json.loads(captured.out.strip())
    assert data["event"] == "analysis_failed"
    assert data["failure_stage"] == "parsing"

def test_analytics_feedback(capsys):
    log_feedback_submitted(is_useful=False, reasons=["Score felt inaccurate"], has_comment=True)
    captured = capsys.readouterr()
    data = json.loads(captured.out.strip())
    assert data["event"] == "feedback_submitted"
    assert data["is_useful"] is False
    assert "Score felt inaccurate" in data["reasons"]
    assert data["has_comment"] is True
