import streamlit as st
from src.analytics import log_feedback_submitted

def show_feedback_ui():
    st.markdown("---")
    st.write("**Was this analysis useful?**")
    
    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False
        
    if not st.session_state.feedback_submitted:
        col1, col2 = st.columns([1, 15])
        with col1:
            if st.button("👍 Yes"):
                log_feedback_submitted(is_useful=True)
                st.session_state.feedback_submitted = True
                st.rerun()
        with col2:
            if st.button("👎 No"):
                st.session_state.show_negative_feedback = True
                
        if st.session_state.get("show_negative_feedback"):
            reasons = st.multiselect(
                "What was wrong?",
                ["Score felt inaccurate", "Missing skill incorrectly detected", "PDF parsing issue", "Recommendation wasn't useful", "Other"]
            )
            comment = st.text_area("Optional comment")
            if st.button("Submit Feedback"):
                log_feedback_submitted(is_useful=False, reasons=reasons, has_comment=bool(comment))
                st.session_state.feedback_submitted = True
                st.rerun()
    else:
        st.success("Thank you for your feedback!")
