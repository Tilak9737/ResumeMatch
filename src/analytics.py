import json
import time
import sys
from typing import Optional

def log_event(event_name: str, **kwargs):
    """
    Structured JSON logger for Streamlit stdout.
    Strictly excludes PII (resume text, JD text, email, IP, filenames).
    """
    payload = {
        "event": event_name,
        "timestamp": time.time(),
    }
    payload.update(kwargs)
    
    # Print as a single JSON line
    print(json.dumps(payload), file=sys.stdout)
    sys.stdout.flush()

def log_analysis_started():
    log_event("analysis_started")

def log_analysis_completed(duration_ms: int, resume_page_count: Optional[int], recommendation_count: int, high_impact_count: int, medium_impact_count: int):
    log_event(
        "analysis_completed", 
        analysis_duration_ms=duration_ms,
        resume_page_count=resume_page_count,
        recommendation_count=recommendation_count,
        high_impact_count=high_impact_count,
        medium_impact_count=medium_impact_count
    )

def log_analysis_failed(failure_stage: str):
    """
    failure_stage: "validation" | "parsing" | "nlp" | "scoring"
    """
    log_event("analysis_failed", failure_stage=failure_stage)

def log_example_loaded():
    log_event("example_loaded")

def log_recommendations_shown():
    log_event("recommendations_shown")

def log_feedback_submitted(is_useful: bool, reasons: list[str] = None, has_comment: bool = False):
    log_event("feedback_submitted", is_useful=is_useful, reasons=reasons, has_comment=has_comment)
