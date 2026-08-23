# ResumeMatch

**See how well your resume matches a job before you apply.**

ResumeMatch is a lightweight Streamlit application that evaluates a resume against a specific job description.

## Architecture and Methodology

ResumeMatch uses a Natural Language Processing (NLP) pipeline leveraging TF-IDF and Cosine Similarity to evaluate resumes. The application employs a **Provisional Scoring Model** (30/30/20/10/10) to break down the match:

*   **Keyword Match (30%)**: Evaluates how well the resume's n-grams match the core requirements of the job description using TF-IDF and cosine similarity.
*   **Experience Level (30%)**: Extracts explicit years of experience from both texts and compares them.
*   **Skills Match (20%)**: Checks for specific tools, languages, and skills mentioned in the JD against a predefined taxonomy and exact text matches.
*   **Education (10%)**: Checks for required degrees (e.g., Bachelor's, Master's) based on keyword extraction.
*   **Formatting/Length (10%)**: Provides a baseline score for resume length and readability.

*Note: The current scoring logic is a provisional implementation (Day 1-3) and serves as a placeholder for more advanced modeling.*

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
4.  Install dependencies: `pip install -r requirements-dev.txt`
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
