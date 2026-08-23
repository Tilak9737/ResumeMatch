import streamlit as st
import os
import tempfile
from src.analysis import analyze_resume_match
from components.error_state import show_error_state
from components.result_card import show_result_card

def main():
    st.set_page_config(page_title="ResumeMatch", page_icon="📄", layout="centered")
    
    st.title("ResumeMatch")
    st.write("See how well your resume matches a job before you apply.")
    
    st.info("**Privacy Notice:** ResumeMatch does not intentionally persist uploaded resumes or job descriptions as part of its application logic. Uploaded files are processed temporarily for analysis and removed after processing. Do not upload sensitive personal information you are uncomfortable processing through a third-party hosted service.", icon="ℹ️")
    
    # Inputs
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description", height=200)
    
    if st.button("Analyze"):
        if not uploaded_file or not jd_text:
            st.warning("Please upload a resume and paste a job description.")
            return
            
        with st.spinner("Analyzing match..."):
            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
                
            try:
                # Run Analysis
                result = analyze_resume_match(tmp_path, jd_text)
                
                # Render results
                if result.errors:
                    show_error_state(result.errors)
                else:
                    show_result_card(result)
            finally:
                # Cleanup temp file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

if __name__ == "__main__":
    main()
