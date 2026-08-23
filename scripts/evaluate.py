import os
import sys
import glob
from src.parser import extract_text_from_pdf
from src.preprocess import clean_text
from src.similarity import calculate_cosine_similarity
from src.keywords import extract_top_keywords
from src.validation import validate_pdf, validate_texts

def evaluate_pair(resume_pdf: str, job_txt: str) -> dict:
    pdf_errors = validate_pdf(resume_pdf)
    if pdf_errors:
        return {"error": pdf_errors}
        
    try:
        resume_raw = extract_text_from_pdf(resume_pdf)
    except Exception as e:
        return {"error": [f"Extraction failed: {str(e)}"]}
        
    with open(job_txt, 'r', encoding='utf-8') as f:
        job_raw = f.read()
        
    text_errors = validate_texts(resume_raw, job_raw)
    if text_errors:
        pass
        
    resume_clean = clean_text(resume_raw)
    job_clean = clean_text(job_raw)
    
    similarity = calculate_cosine_similarity(resume_clean, job_clean)
    resume_keywords = extract_top_keywords(resume_clean)
    job_keywords = extract_top_keywords(job_clean)
    
    return {
        "similarity": similarity,
        "resume_keywords": resume_keywords,
        "job_keywords": job_keywords
    }

def main():
    base_dir = "data/examples"
    if not os.path.exists(base_dir):
        print(f"{base_dir} not found.")
        sys.exit(1)
        
    pairs = glob.glob(os.path.join(base_dir, "pair_*"))
    for pair_dir in sorted(pairs):
        resume_pdf = os.path.join(pair_dir, "resume.pdf")
        job_txt = os.path.join(pair_dir, "job.txt")
        
        if not os.path.exists(resume_pdf) or not os.path.exists(job_txt):
            continue
            
        print(f"--- Evaluating {os.path.basename(pair_dir)} ---")
        result = evaluate_pair(resume_pdf, job_txt)
        if "error" in result:
            print(f"Errors: {result['error']}")
        else:
            print(f"Similarity: {result['similarity']:.2f}%")
            print(f"Resume Keywords: {result['resume_keywords'][:5]}")
            print(f"Job Keywords: {result['job_keywords'][:5]}")
        print()

if __name__ == "__main__":
    main()
