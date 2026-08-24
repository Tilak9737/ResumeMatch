import streamlit as st
from src.models import AnalysisResult

def show_score_breakdown(result: AnalysisResult):
    st.markdown("### WHY THIS SCORE?")
    
    skills_cov = (len(result.matched_skills) / len(result.job_skills) * 100.0) if result.job_skills else 100.0
    
    # Similarity
    st.write(f"**Similarity** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {result.similarity_score:.0f}%")
    st.progress(min(result.similarity_score / 100.0, 1.0))
    
    # Keyword coverage
    st.write(f"**Keyword coverage** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {result.keyword_coverage:.0f}%")
    st.progress(min(result.keyword_coverage / 100.0, 1.0))
    
    # Skills overlap
    st.write(f"**Skills overlap** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {skills_cov:.0f}%")
    st.progress(min(skills_cov / 100.0, 1.0))
    
    # Required coverage
    st.write(f"**Required coverage** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {result.required_term_coverage:.0f}%")
    st.progress(min(result.required_term_coverage / 100.0, 1.0))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("Show detailed calculation"):
        st.markdown("""
        **The Provisional Match Score is calculated as follows:**
        
        `(30 × Keyword Coverage + 30 × TF-IDF Similarity + 20 × Skills Overlap + 10 × Required-Term Coverage) / 90`
        """)
