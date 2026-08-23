import streamlit as st

def show_error_state(errors: list[str]):
    """Renders clear error states to the user if validation or parsing fails."""
    if not errors:
        return
        
    st.error("Analysis could not be completed due to the following errors:")
    for error in errors:
        st.write(f"- {error}")
