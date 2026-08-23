import streamlit as st
from src.models import AnalysisResult

def show_result_card(result: AnalysisResult):
    """Renders the matched score and core signals based on the AnalysisResult."""
    st.header("Analysis Results")
    
    st.metric(label="Resume–Job Similarity", value=f"{result.similarity_score:.1f}%")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Matching Terms")
        if result.matched_keywords:
            for kw in result.matched_keywords[:10]: # show top 10
                st.write(f"✅ {kw}")
        else:
            st.write("None")
            
    with col2:
        st.subheader("Potentially Missing Terms")
        if result.missing_keywords:
            for kw in result.missing_keywords[:10]: # show top 10
                st.write(f"❌ {kw}")
        else:
            st.write("None")
