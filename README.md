# ResumeMatch

**See how well your resume matches a job before you apply.**

ResumeMatch is a lightweight Streamlit application that evaluates a resume against a specific job description.

## Architecture and Methodology

ResumeMatch uses a Natural Language Processing (NLP) pipeline leveraging TF-IDF and Cosine Similarity to evaluate resumes. The application employs a **Provisional Scoring Model** (Day 4) to break down the match:

**Day 4 Provisional Model**
*   **Keyword Coverage** 30%
*   **TF-IDF Similarity** 30%
*   **Skills Overlap** 20%
*   **Required Coverage** 10%
*   **Experience/Education** 10% [Deferred]

*Note: The final 10% Experience/Education component is not active in Day 3/4. The active score is normalized over the implemented 90%: `(30×keyword + 30×similarity + 20×skills + 10×required) / 90`*

## Limitations

*   **Not an ATS Predictor**: This tool is designed for feedback and alignment, not to predict how a specific Applicant Tracking System (ATS) will parse or score your resume. Different ATS platforms use proprietary logic.
*   **Rule-Based Extraction**: Some extractions (like years of experience) rely on regular expressions and might miss complex phrasing.
*   **Skill Taxonomy**: The underlying skill taxonomy is basic and may not cover niche or emerging skills perfectly.

## Local Installation

1.  Clone the repository.
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the environment:
    *   Windows: `venv\Scripts\activate`
    *   Mac/Linux: `source venv/bin/activate`
4.  Install dependencies:
    *   **Production**: `pip install -r requirements.txt`
    *   **Development/Testing**: `pip install -r requirements-dev.txt`
5.  Run the application: `streamlit run app.py`
6.  Run tests: `pytest`

## Deployment

The application is designed to be easily deployed on Streamlit Community Cloud:
1. Push the code to a GitHub repository.
2. Log in to Streamlit Community Cloud.
3. Create a new app, point it to your repository, branch, and select `app.py` as the main file.
4. Deploy!

## Privacy Notice

ResumeMatch does not intentionally persist uploaded resumes or job descriptions as part of its application logic. Uploaded files are processed temporarily for analysis and removed after processing. Do not upload sensitive personal information you are uncomfortable processing through a third-party hosted service.
