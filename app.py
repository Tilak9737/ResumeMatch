import streamlit as st
import os
import tempfile
from src.analysis import analyze_resume_match
from components.error_state import show_error_state
from components.result_card import show_result_card
from src.analytics import log_example_loaded

EXAMPLE_JD = """Junior Data Scientist
Required Skills:
- Python
- SQL
- Data Analysis

Preferred Skills:
- Docker
- Machine Learning

We are looking for an analytical thinker who can help us make sense of our data."""

EXAMPLE_RESUME = """Data Analyst
Skills: Python, MySQL, Data Analysis, Power BI, Statistics.

Experience:
- Analyzed large datasets using Python and pandas.
- Maintained MySQL databases and wrote complex queries.
- Built interactive dashboards."""

def main():
    st.set_page_config(page_title="ResumeMatch", page_icon="📄", layout="centered")
    
    # Minimal Editorial Copy
    st.markdown("<h1 style='text-align: left;'>ResumeMatch</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.2rem; color: #4A4A4A;'>See how well your resume matches a job before you apply.<br>Upload your resume and paste the job description.<br>Get a transparent analysis in seconds.</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # State for Example Flow
    if "example_loaded" not in st.session_state:
        st.session_state.example_loaded = False
        st.session_state.jd_text_input = ""
        
    # Inputs
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
    with col2:
        st.write("") # spacing
        st.write("")
        if st.button("Try an example →"):
            st.session_state.example_loaded = True
            st.session_state.jd_text_input = EXAMPLE_JD
            log_example_loaded()
            st.rerun()
            
    if st.session_state.example_loaded:
        st.success("Example Data Analyst Resume loaded.")
            
    st.markdown("### Job description")
    jd_text = st.text_area("Paste the job description here...", height=200, value=st.session_state.jd_text_input)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Analyze Resume", type="primary"):
        if not uploaded_file and not st.session_state.example_loaded:
            st.warning("Please upload a resume or try an example.")
            return
        if not jd_text:
            st.warning("Please paste a job description.")
            return
            
        with st.spinner("Analyzing match..."):
            result = None
            if st.session_state.example_loaded and not uploaded_file:
                # Use example text
                result = analyze_resume_match(resume_text=EXAMPLE_RESUME, jd_text=jd_text)
            else:
                # Save uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                    
                try:
                    result = analyze_resume_match(resume_pdf_path=tmp_path, jd_text=jd_text)
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
            
            # Render results
            st.markdown("---")
            if result and result.errors:
                show_error_state(result.errors)
            elif result:
                show_result_card(result)

if __name__ == "__main__":
    main()
