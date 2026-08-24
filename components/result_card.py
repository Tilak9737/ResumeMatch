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
    
    st.markdown("**MATCHED**")
    if result.matched_skills:
        for sk in result.matched_skills:
            st.write(f"✓ {sk}")
    else:
        st.write("None")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**WEAK EVIDENCE**")
    if result.weak_evidence:
        for sk in result.weak_evidence:
            st.write(f"◐ {sk}")
    else:
        st.write("None")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**MISSING**")
    if result.missing_skills:
        for sk in result.missing_skills:
            st.write(f"× {sk}")
    else:
        st.write("None")
        
    st.markdown("---")
    
    # Recommendations
    st.markdown("### What should I change?")
    log_recommendations_shown()
    
    high_impact = [r for r in result.recommendations if r.impact == "HIGH"]
    medium_impact = [r for r in result.recommendations if r.impact == "MEDIUM"]
    low_impact = [r for r in result.recommendations if r.impact == "LOW"]
    
    if not high_impact and not medium_impact and not low_impact:
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

    show_feedback_ui()
