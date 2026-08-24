import streamlit as st
from src.models import AnalysisResult
from .score_breakdown import show_score_breakdown
from .feedback import show_feedback_ui
from src.analytics import log_recommendations_shown

def _get_human_explanation(result: AnalysisResult) -> str:
    skills_cov = (len(result.matched_skills) / len(result.job_skills) * 100.0) if result.job_skills else 100.0
    
    strongest = "Similarity"
    strongest_val = result.similarity_score
    if result.keyword_coverage > strongest_val:
        strongest = "Keyword coverage"
        strongest_val = result.keyword_coverage
    if skills_cov > strongest_val:
        strongest = "Skills overlap"
        strongest_val = skills_cov
    if result.required_term_coverage > strongest_val:
        strongest = "Required terms coverage"
        
    return f"Your strongest area is {strongest.lower()}."

def show_result_card(result: AnalysisResult):
    """Renders the comprehensive analysis report."""
    
    # Overall Score Header
    st.markdown("## Analysis complete")
    
    st.markdown("### Resume ↔ Job Match")
    st.markdown(f"<h1 style='font-size: 3rem;'>{result.provisional_score:.0f}%</h1>", unsafe_allow_html=True)
    
    if result.provisional_score >= 80:
        st.markdown("**Strong alignment**")
    elif result.provisional_score >= 60:
        st.markdown("**Good alignment**")
    else:
        st.markdown("**Weak alignment**")
        
    st.caption("Based on 90% of the planned scoring framework. Experience/Education analysis is not yet active.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.write(_get_human_explanation(result))
    
    st.markdown("---")
    
    # Score Breakdown
    show_score_breakdown(result)
    
    st.markdown("---")
    
    # Evidence
    st.markdown("### Skills & Evidence")
    
    matched_ev = [e for e in result.evidence if e.evidence_level == "MATCHED"]
    weak_ev = [e for e in result.evidence if e.evidence_level == "WEAK"]
    missing_ev = [e for e in result.evidence if e.evidence_level == "MISSING"]
    
    st.markdown("**MATCHED**")
    if matched_ev:
        for e in matched_ev:
            st.markdown(f"✓ **{e.skill}** <span style='color: #666; font-size: 0.9em;'>· {e.evidence_source}</span>", unsafe_allow_html=True)
    else:
        st.write("None")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**WEAK EVIDENCE**")
    if weak_ev:
        for e in weak_ev:
            st.markdown(f"◐ **{e.skill}** <span style='color: #666; font-size: 0.9em;'>· {e.evidence_source}</span>", unsafe_allow_html=True)
    else:
        st.write("None")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**MISSING**")
    if missing_ev:
        for e in missing_ev:
            req_type_str = "(Required)" if e.requirement_type == "REQUIRED" else "(Preferred)"
            st.markdown(f"× **{e.skill}** <span style='color: #666; font-size: 0.9em;'>{req_type_str}</span>", unsafe_allow_html=True)
    else:
        st.write("None")
        
    st.markdown("---")
    
    # Recommendations
    st.markdown("### What should I change?")
    log_recommendations_shown()
    
    if "show_all_recs" not in st.session_state:
        st.session_state.show_all_recs = False
    
    all_high_impact = [r for r in result.recommendations if r.impact == "HIGH"]
    all_medium_impact = [r for r in result.recommendations if r.impact == "MEDIUM"]
    all_low_impact = [r for r in result.recommendations if r.impact == "LOW"]
    
    hidden_count = max(0, len(all_high_impact) - 2) + max(0, len(all_medium_impact) - 3) + max(0, len(all_low_impact) - 2)
    
    if st.session_state.show_all_recs:
        high_impact = all_high_impact
        medium_impact = all_medium_impact
        low_impact = all_low_impact
    else:
        high_impact = all_high_impact[:2]
        medium_impact = all_medium_impact[:3]
        low_impact = all_low_impact[:2]
    
    if not all_high_impact and not all_medium_impact and not all_low_impact:
        st.write("Your resume looks great! No immediate changes recommended.")
        
    for rec in high_impact:
        st.markdown(f"**🔴 {rec.action}**<br><span style='color: #555;'>{rec.evidence_type}</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
    for rec in medium_impact:
        st.markdown(f"**🟡 {rec.action}**<br><span style='color: #555;'>{rec.evidence_type}</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
    for rec in low_impact:
        st.markdown(f"**⚪ {rec.action}**<br><span style='color: #555;'>{rec.evidence_type}</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    if hidden_count > 0 and not st.session_state.show_all_recs:
        if st.button(f"Show {hidden_count} more recommendations"):
            st.session_state.show_all_recs = True
            st.rerun()
    elif st.session_state.show_all_recs and hidden_count > 0:
        if st.button("Show fewer recommendations"):
            st.session_state.show_all_recs = False
            st.rerun()

    show_feedback_ui()
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.85rem; color: #777;">
    <b>Limitations:</b> This analysis uses a localized keyword and TF-IDF similarity model. It does not perfectly understand semantic context or complex sentence structures. Always tailor your resume manually for the best results. No personally identifiable information (PII) is stored or retained.
    </div>
    """, unsafe_allow_html=True)
